/*
  This software is Copyright (C) 2021-2022 by Ben Cahill and 2006-2022 by James C. Ahlstrom,
  and is licensed for use under the GNU General Public License (GPL).
  See http://www.opensource.org.
  Note that there is NO WARRANTY AT ALL.  USE AT YOUR OWN RISK!!
*/

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <complex.h>
#include <math.h>
#include <sys/time.h>
#include <time.h>
#include <errno.h>

#ifdef MS_WINDOWS
#include <winsock2.h>
#include <stdint.h>
#else
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <fcntl.h>
#endif

#include "../quisk.h"

#define GRAPH_DATA_SCALE	163
#define GRAPH_DATA_BLOCK	600

#define REMOTE_DEBUG 0  //BMC TODO:  Make this a configuration option

// For remote control sound; 2 sockets used at each end, but 4 needed to guide program flow
static SOCKET radio_sound_to_control_head_socket = INVALID_SOCKET;	// send radio sound to control_head
static SOCKET radio_sound_from_remote_radio_socket = INVALID_SOCKET;	// receive radio sound from remote_radio
static SOCKET mic_sound_from_control_head_socket = INVALID_SOCKET;	// receive mic sound from control_head
static SOCKET mic_sound_to_remote_radio_socket = INVALID_SOCKET;	// send mic sound to remote_radio
static SOCKET graph_data_to_control_head_socket = INVALID_SOCKET;	// send graph data to control_head
static SOCKET graph_data_from_remote_radio_socket = INVALID_SOCKET;	// receive graph data from remote_radio
static int sound_from_remote_socket_started = 0;			// sound (radio or mic) stream started from far end
static int sound_to_remote_socket_started = 0;				// sound (radio or mic) stream started from near end
static int graph_from_remote_socket_started = 0;			// graph data stream started from far end
static int graph_to_remote_socket_started = 0;				// graph data stream started from near end
static int control_head_data_width;					// app.data_width of control head for graph data
static int packets_sent;
static int packets_recd;
//static struct sockaddr_in AddrControlHeadGraph;				// socket address of control head graph data port

static void send_remote_sound_socket(SOCKET * sock, complex double * cSamples, int nSamples);

// Receive stereo 16-bit pcm sound via UDP
// This code acts as UDP client for radio sound (on control head)
int read_remote_radio_sound_socket(struct sound_dev* dev, complex double * cSamples, int nSamples)
{
	int i;
	int bytes = 0;
	double samp_r, samp_l;
	int16_t * ptInt16;
	int lapcount = 0;
	struct timeval tm_wait;
	fd_set fds;
	SOCKET * sock = &radio_sound_from_remote_radio_socket;
	// static okay if only one instance runs, which should be good assumption when running remote
	static char buf[128000];	// TODO:  Calculate based on remote sound latency setting
	static int prebuf_samples = 48000 / 10; // 100 msec (TODO:  replace with calculation)
	static int prebuf_done = 0;
	static int rd_idx = 0;	// bytes
	static int wr_idx = 0;	// bytes
	static int wrap_idx;	// bytes
	static int samps_in_buf = 0;	// samples (4 bytes per sample)
	static int underrun_count = 0;	// samples
	static size_t prior_pkt_size_max = 0;

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls
	// measure/monitor tools:
	static float callcount = 0;
	static float sampcount_in = 0;
	static float sampcount_out = 0;
	static float nSamps = 0;
	static uint64_t bunchcount = 0;
	static float callcount_total = 0;
	static float sampcount_in_total = 0;
	static float sampcount_out_total = 0;
	static float nSamps_total = 0;
	static double delta_total = 0;
	static double prior_ts = 0;
#endif

	if (*sock == INVALID_SOCKET)
		return 0;

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls
	nSamps += nSamples;
	callcount++;
#endif
	// Signal far end (server) that we're ready (this sends our address/port to far end)
	if (!sound_from_remote_socket_started) {
		QuiskPrintf("read_remote_radio_sound_socket() sending 'rr', *sock = %u\n", (u_int)*sock);
		bytes = send(*sock, "rr\n", 3, 0);
		if (bytes != 3)
			QuiskPrintf("read_remote_radio_sound_socket(), sendto(): %s\n", strerror(errno));
	}

	// read all available packets, one per loop, place into jitter-absorbing circular buffer
	while (1) {
		int buftop;
		char * wr_base;
		size_t wr_len;
		lapcount++;
		// set up for direct receive into circular buffer
		wr_base = &buf[wr_idx];
		if (wr_idx > rd_idx || samps_in_buf == 0)
			buftop = sizeof(buf);
		else
			buftop = rd_idx;
		wr_len = buftop - wr_idx;	// contiguous (non-wrapping) space available in buffer
		if (wr_len < prior_pkt_size_max && prior_pkt_size_max > 0) {
			if (wr_idx > rd_idx || samps_in_buf == 0) {
				// wrap before recv() so data expected in recv() fits within contiguous (non-wrapping) space
				wrap_idx = wr_idx;
				wr_idx = 0;
				wr_base = &buf[0];
				if (samps_in_buf == 0)
					wr_len = sizeof(buf);
				else
					wr_len = rd_idx;
#if REMOTE_DEBUG > 2 //BMC debug
				QuiskPrintf("wrapping write at wrap_idx = %i, rd_idx = %i, wr_len = %li\n", wrap_idx, rd_idx, wr_len);
#endif
			}
#if REMOTE_DEBUG > 0
			else {
				double now = QuiskTimeSec();
				QuiskPrintf("%f, jitbuf overflow, reduce recv fm %u to %u, wr_idx %u, rd_idx %u, samps_in_buf %u, remainder 0s\n",
					now, (u_int)prior_pkt_size_max, (u_int)wr_len, wr_idx, rd_idx, samps_in_buf);
			}
#endif
		}

		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if (select(*sock + 1, &fds, NULL, NULL, &tm_wait) != 1) {
			//BMC QuiskPrintf("read_remote_radio_sound_socket(): select returned %i\n", retval);
			bytes = 0;
			break;
		}
		bytes = recv(*sock, wr_base, wr_len, 0);
		if (bytes < 0) {
			int err = errno;
			if (err != EAGAIN && err != EWOULDBLOCK)
				QuiskPrintf("read_remote_radio_sound_socket(), recv(): %s\n", strerror(errno));
			break;
		}
		if (bytes > 0) {
			sound_from_remote_socket_started = 1;
			packets_recd++;
			wr_idx += bytes;
			if ((size_t)bytes > prior_pkt_size_max)
				prior_pkt_size_max = bytes;
			samps_in_buf += bytes / 4;	//TODO:  Calculate using sizeof
#if REMOTE_DEBUG > 0 //BMC debug -- for summary every 200 calls
			sampcount_in += bytes / 4;
#endif
		}
	} // while(1)
	if (!sound_from_remote_socket_started  && bytes > 0) {
		QuiskPrintf("read_remote_radio_sound_socket(): Started! samps_in_buf = %i\n", bytes / 4);
		sound_from_remote_socket_started = 1;
	}
	if (!prebuf_done) {
		if (samps_in_buf >= prebuf_samples) {
			prebuf_done = 1;
			QuiskPrintf("read_remote_radio_sound_socket: Prebuf done, samps_in_buf = %i\n", samps_in_buf);
		}
	}

	if (quisk_play_state > RECEIVE && dev->dev_index == t_Playback) {
		// TX time for Radio Sound client ...
		if (samps_in_buf > prebuf_samples * 2 && underrun_count > prebuf_samples / 4) {
			// Network delays may cause radio sound jitter buffer underruns, but the incoming sound samples eventually
			// arrive from the network, causing the jitter buffer to contain *more* samples than desired,
			// perhaps even causing jitbuf overflows (so don't use underrun_count to calculate # samples to remove).
			// Use Tx time to remove excess samples to keep playback latency short;
			//     set rd_idx so there is prebuf_samples number of samples in buffer.
#if REMOTE_DEBUG > 0
			double now = QuiskTimeSec();
			QuiskPrintf("%f, Removing excess jitbuf samples: underrun_count %i, samps_in_buf %i, rd_idx %i, wrap_idx %i, wr_idx %i\n",
					now, underrun_count, samps_in_buf, rd_idx, wrap_idx, wr_idx);
#endif
			rd_idx = wr_idx - (prebuf_samples * 4);	// rd_idx = bytes; prebuf_samples = samples; 4 bytes per sample
			if (rd_idx < 0)
				rd_idx += wrap_idx;
			samps_in_buf = prebuf_samples;
			underrun_count = 0;
#if REMOTE_DEBUG > 0
			QuiskPrintf("%f, Removed excess jitbuf samples: samps_in_buf %i, rd_idx %i, wrap_idx %i,\n",
					now, samps_in_buf, rd_idx, wrap_idx);
#endif
		}
		if (quisk_active_sidetone == 4) {
			// Overwrite remote sound with sidetone, starting at jitter buffer read position
			int tmp_idx = rd_idx;
			ptInt16 = (int16_t *)&buf[tmp_idx];
			for (i = 0; i < nSamples; i++) {
				int16_t * ptSamples = quisk_make_sidetone(dev, 0);
				*ptInt16++ = *ptSamples;
				*ptInt16++ = *ptSamples;
				tmp_idx += 4;
				if (tmp_idx >= wrap_idx && wrap_idx != 0) {
					tmp_idx = 0;
					ptInt16 = (int16_t *)&buf[tmp_idx];
#if 0 //BMC debug
					QuiskPrintf("wrapping sidetone at wrap_idx = %i\n", wrap_idx);
#endif
				}
			}
		}
	}


	if (prebuf_done) {
		int numout = nSamples;
		int newSamples = 0;
		if (samps_in_buf < nSamples) {
			double now = QuiskTimeSec();
			numout = samps_in_buf;
			underrun_count += (nSamples - samps_in_buf);
			QuiskPrintf("%f, jitbuf low, reduce outsamps fm %i to %i, wr_idx %i, rd_idx %i, samps_in_buf %i, remainder 0s\n",
				now, nSamples, numout, wr_idx, rd_idx, samps_in_buf);
		}
		ptInt16 = (int16_t *)&buf[rd_idx];
		for (i = 0; i < numout; i++) {
			samp_r = *ptInt16++;
			samp_l = *ptInt16++;
			cSamples[newSamples++] = (samp_r + I * samp_l) / CLIP16 * CLIP32;
#if REMOTE_DEBUG > 0 //BMC debug -- for summary every 200 calls
			sampcount_out++;
#endif
			samps_in_buf--;
			rd_idx += 4;
			if (rd_idx >= wrap_idx && wrap_idx != 0) {
				rd_idx = 0;
				ptInt16 = (int16_t *)&buf[rd_idx];
#if REMOTE_DEBUG > 2 //BMC debug
				QuiskPrintf("wrapping read at wrap_idx = %i\n", wrap_idx);
#endif
			}
		}
	}

#if REMOTE_DEBUG > 1 //BMC debug -- per-call (perhaps multi-packet) statistics
	if (lapcount != 1) {	// 1: 0 packets, 2: 1 packet, 3: 2 packets, etc.
		double ts = QuiskTimeSec();
		QuiskPrintf("%f: callcount = %lu, lapcount = %i, bytes = %i, nSamples = %i\n", ts, callcount, lapcount, bytes, nSamples);
	}
#endif

#if REMOTE_DEBUG > 0 //BMC debug -- summary every 200 calls (a little over one second)
	if (callcount >= 200) {
		double new_ts = QuiskTimeSec();
		double delta = new_ts - prior_ts;
		prior_ts = new_ts;
#if REMOTE_DEBUG > 2 //BMC raw numbers
		QuiskPrintf("%f: read_remote_radio_sound_socket CURRENT calls: %lu, samps_in %lu, samps_out %lu, nSamps %lu, samps_in_buf %i, deltasec %f\n",
			new_ts, callcount, sampcount_in, sampcount_out, nSamps, samps_in_buf, delta);
#endif
#if REMOTE_DEBUG > 1 //BMC raw numbers
		QuiskPrintf("%f: read_remote_radio_sound_socket CURRENT RATES (HZ): calls %f, samps_in %f, samps_out %f, nSamps %f, samps_in_buf %i\n",
			new_ts, callcount / delta, sampcount_in / delta, sampcount_out / delta, nSamps / delta, samps_in_buf);
#endif
		if (bunchcount > 0) {	// skip the initial bunch; prebuf may distort some numbers(?)
			callcount_total += callcount;
			sampcount_in_total += sampcount_in;
			sampcount_out_total += sampcount_out;
			nSamps_total += nSamps;
			delta_total += delta;
		}
		if (bunchcount % 10 == 0 && bunchcount > 0) {
#if REMOTE_DEBUG > 1 //BMC
			QuiskPrintf("%f: read_remote_radio_sound_socket SUMMARY calls: %f, samps_in %f, samps_out %f, nSamps %f, samps_in_buf %i, deltasec %f\n",
				new_ts, callcount_total, sampcount_in_total, sampcount_out_total, nSamps_total, samps_in_buf, delta_total);
			QuiskPrintf("%f: read_remote_radio_sound_socket SUMMARY RATES (HZ): calls %f, samps_in %f, samps_out %f, nSamps %f\n",
				new_ts, callcount_total / delta_total, sampcount_in_total / delta_total,
				sampcount_out_total / delta_total, nSamps_total / delta_total);
#else
			float latency = (float)samps_in_buf / 48000.0;
			QuiskPrintf("%f: read_remote_radio_sound_socket samps_in_buf %i, latency %f sec\n", new_ts, samps_in_buf, latency);
#endif
		}
		bunchcount++;
		callcount = 0;
		sampcount_in = 0;
		sampcount_out = 0;
		nSamps = 0;
	}
#endif
	// Always return same # samples sent in, even if we didn't change any
	return nSamples;
}



// Receive stereo 16-bit pcm sound via UDP
// This code acts as UDP client for mic sound (on remote radio)
int read_remote_mic_sound_socket(struct sound_dev* dev, complex double * cSamples)
{
	int i;
	int bytes = 0;
	double samp_r, samp_l;
	int16_t * ptInt16;
	int rd_idx = 0;	// bytes
	int wr_idx = 0;	// bytes
	int samps_in_buf = 0;	// samples (4 bytes per sample)
	int lapcount = 0;
	struct timeval tm_wait;
	fd_set fds;
	SOCKET * sock = &mic_sound_from_control_head_socket;
	// static okay if only one instance runs, which should be good assumption when running remote
	static char buf[128000];	// TODO:  Calculate based on ???

	if (*sock == INVALID_SOCKET)
		return 0;

	// Signal far end (server) that we're ready (this sends our address/port to far end)
	if (!sound_from_remote_socket_started) {
		QuiskPrintf("read_remote_mic_sound_socket() sending 'rr', *sock = %u\n", (u_int)*sock);
		bytes = send(*sock, "rr\n", 3, 0);
		if (bytes != 3)
			QuiskPrintf("read_remote_mic_sound_socket(), sendto(): %s\n", strerror(errno));
	}

	// read all available packets, one per loop, place into jitter-absorbing circular buffer
	while (1) {
		int buftop = sizeof(buf);
		char * wr_base;
		size_t wr_len;
		lapcount++;
		// set up for direct receive into linear buffer
		wr_base = &buf[wr_idx];
		wr_len = buftop - wr_idx;	// remaining contiguous space available in buffer

		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if (select(*sock + 1, &fds, NULL, NULL, &tm_wait) != 1) {
			//BMC QuiskPrintf("read_remote_mic_sound_socket(): select returned %i\n", retval);
			bytes = 0;
			break;
		}
		bytes = recv(*sock, wr_base, wr_len, 0);
		if (bytes < 0) {
			int err = errno;
			if (err != EAGAIN && err != EWOULDBLOCK)
				QuiskPrintf("read_remote_mic_sound_socket(), recv(): %s\n", strerror(errno));
			break;
		}
		if (bytes > 0) {
			sound_from_remote_socket_started = 1;
			packets_recd++;
			wr_idx += bytes;
			samps_in_buf += bytes / 4;	//TODO:  Calculate using sizeof
		}
	} // while(1)

	if (!sound_from_remote_socket_started  && bytes > 0) {
		QuiskPrintf("read_remote_mic_sound_socket(): Started! samps_in_buf = %i\n", bytes / 4);
		sound_from_remote_socket_started = 1;
	}

	ptInt16 = (int16_t *)&buf[rd_idx];
	for (i = 0; i < samps_in_buf; i++) {
		samp_r = *ptInt16++;
		samp_l = *ptInt16++;
		cSamples[i] = (samp_r + I * samp_l) / CLIP16 * CLIP32;
		rd_idx += 4;
	}

	return samps_in_buf;
}
// Send stereo 16-bit pcm sound via UDP
// This code acts as UDP server for radio sound (on remote radio) or mic sound (on control head)
#define MAX_SAMPLES_FOR_REMOTE_SOUND 15000
#define RX_BUFFER_SIZE 64

void send_remote_radio_sound_socket(complex double * cSamples, int nSamples)
{
	send_remote_sound_socket(&radio_sound_to_control_head_socket, cSamples, nSamples);
}

void send_remote_mic_sound_socket(complex double * cSamples, int nSamples)
{
	send_remote_sound_socket(&mic_sound_to_remote_radio_socket, cSamples, nSamples);
}

static void send_remote_sound_socket(SOCKET * sock, complex double * cSamples, int nSamples)
{	// Send nSamples samples.  Each sample is sent as two shorts (4 bytes) of L/R audio data.
	int i, sent;
	short sound_lr[MAX_SAMPLES_FOR_REMOTE_SOUND * 2]; // Limit Tx to 60,000 bytes, 30,000 shorts, 15,000 samples
	int udp_size = 0;	// Keep track of UDP payload size, in shorts
	char buf[RX_BUFFER_SIZE];	// For startup message
	int recv_len;
	int retval;

#if REMOTE_DEBUG > 0 //BMC debug
	// measure/monitor tools:
	static float callcount = 0;
	static float sampcount = 0;
	static uint64_t bunchcount = 0;
	static float callcount_total = 0;
	static float sampcount_total = 0;
	static double prior_ts = 0;
	static double delta_total = 0;
#if REMOTE_DEBUG > 1 //BMC debug
	static double prior_packet_ts = 0.0;
	double now;
#endif
#endif

	if (*sock == INVALID_SOCKET)
		return;

#if REMOTE_DEBUG > 0 //BMC debug
	callcount++;
#endif
	// Wait for far end (client) to send its opening greetings, so we can grab its network address/port
	if (!sound_to_remote_socket_started) {
		struct sockaddr_in far_addr;
#ifdef MS_WINDOWS
		int addr_len = sizeof(struct sockaddr_in);
#else
		socklen_t addr_len = sizeof(struct sockaddr_in);
#endif
		struct timeval tm_wait;
		fd_set fds;
		tm_wait.tv_sec = 0;
		tm_wait.tv_usec = 0;
		FD_ZERO (&fds);
		FD_SET (*sock, &fds);
		if ((retval = select(*sock + 1, &fds, NULL, NULL, &tm_wait)) != 1) {
			//BMC QuiskPrintf("send_remote_sound_socket(): select returned %i\n", retval);
			return;
		}
		// Receive short msg, grab far end address
		if ((recv_len = recvfrom(*sock, buf, RX_BUFFER_SIZE, 0, (struct sockaddr *) &far_addr, &addr_len)) == -1) {
			QuiskPrintf("send_remote_sound_socket(), recvfrom(): %s\n", strerror(errno));
			return;
		}
		else if(recv_len > 0) {
			if (recv_len >= RX_BUFFER_SIZE)
				buf[RX_BUFFER_SIZE - 1] = '\n';
			else
				buf[recv_len] = '\n';
			QuiskPrintf("send_remote_sound_socket(): recv_len = %i, %s", recv_len, buf);
			if (connect(*sock, (const struct sockaddr *)&far_addr, sizeof(far_addr)) != 0) {
				QuiskPrintf("send_remote_sound_socket), connect(): %s\n", strerror(errno));
				close(*sock);
				*sock = INVALID_SOCKET;
			}
			else
				sound_to_remote_socket_started = 1;
		}
	}

	if (nSamples > MAX_SAMPLES_FOR_REMOTE_SOUND) {
		QuiskPrintf("send_remote_sound_socket():  nSamples %i > MAX_SAMPLES_FOR_REMOTE_SOUND 15,000, trimming to MAX\n", nSamples);
		nSamples = MAX_SAMPLES_FOR_REMOTE_SOUND;
	}

	// Convert format from complex double to stereo pairs of 16-bit PCM samples, send to client
	for (i = 0; i < nSamples; i++) {
		sound_lr[udp_size++] = (short)(creal(cSamples[i]) * (double)CLIP16 / CLIP32);
		sound_lr[udp_size++] = (short)(cimag(cSamples[i]) * (double)CLIP16 / CLIP32);
	}
	if (udp_size > 0) {
		sent = send(*sock, (char *)sound_lr, udp_size * 2, 0);
		if (sent != udp_size * 2)
			QuiskPrintf("send_remote_sound_socket(), send(): %s\n", strerror(errno));
#if REMOTE_DEBUG > 0 //BMC debug
		else {
			sampcount += sent/4;
			packets_sent++;
#if REMOTE_DEBUG > 1 //BMC debug
			now = QuiskTimeSec();
			QuiskPrintf("%f, send_remote_sound_socket(): now - prior = %f, samples = %u, sampcount = %lu\n",
				now, now - prior_packet_ts, sent / 4, sampcount);
			prior_packet_ts = now;
#endif
		}
#endif
	}
#if REMOTE_DEBUG > 1 //BMC debug
	else {
		now = QuiskTimeSec();
		QuiskPrintf("%f, send_remote_sound_socket(): nSamples = %i\n", now, nSamples);
	}
#endif
#if REMOTE_DEBUG > 0 //BMC debug
	if (callcount >= 200) {
		double new_ts = QuiskTimeSec();
		double delta = new_ts - prior_ts;
		prior_ts = new_ts;
#if REMOTE_DEBUG > 1 //BMC every 200
		QuiskPrintf("send_remote_sound_socket CURRENT calls: %lu, samples %lu, deltasec %f\n", callcount, sampcount, delta);
		QuiskPrintf("%f: send_remote_sound_socket CURRENT RATES (HZ): calls %f, samples %f\n", new_ts, callcount / delta, sampcount / delta);
#endif
		if (bunchcount > 0) {	// skip the initial bunch; prebuf may distort some numbers(?)
			callcount_total += callcount;
			sampcount_total += sampcount;
			delta_total += delta;
		}
		if (bunchcount % 10 == 0 && bunchcount > 0) {
			QuiskPrintf("%f: send_remote_sound_socket SUMMARY calls: %f, samples %f, deltasec %f\n",
				new_ts, callcount_total, sampcount_total, delta_total);
			QuiskPrintf("%f: send_remote_sound_socket SUMMARY RATES (HZ): calls %f, samples %f\n",
				new_ts, callcount_total / delta_total, sampcount_total / delta_total);
		}
		bunchcount++;
		callcount = 0;
		sampcount = 0;
	}
#endif
}

void send_graph_data(double * fft_avg, int fft_size, double zoom, double deltaf, int fft_sample_rate, double scale)
{  // called by the sound thread
	static double * pixels = NULL;
	static int n_pixels = 0;
	static uint8_t sequence = 0;
	uint8_t flags;
	int16_t buffer[GRAPH_DATA_BLOCK];
	int16_t block;
	int pixel_index, buffer_index;
	double d1, d2;
	ssize_t sent;
	char buf[RX_BUFFER_SIZE];	// For startup message
	int recv_len;
	struct sockaddr_in far_addr;
#ifdef MS_WINDOWS
	int addr_len = sizeof(struct sockaddr_in);
#else
	socklen_t addr_len = sizeof(struct sockaddr_in);
#endif

	if (graph_data_to_control_head_socket == INVALID_SOCKET)
		return;
	if ( !control_head_data_width)
		return;
	if ( !graph_to_remote_socket_started) {
		// Receive short msg, grab far end address
		// Receive from control head is necessary to establish a path through NAT
		if ((recv_len = recvfrom(graph_data_to_control_head_socket, buf, RX_BUFFER_SIZE, 0, (struct sockaddr *) &far_addr, &addr_len)) < 2) {
			return;
		}
		else {
			if (connect(graph_data_to_control_head_socket, (const struct sockaddr *)&far_addr, sizeof(far_addr)) != 0) {
				QuiskPrintf("send_remote_graph_socket), connect(): %s\n", strerror(errno));
				close(graph_data_to_control_head_socket);
				graph_data_to_control_head_socket = INVALID_SOCKET;
				return;
			}
			else {
				graph_to_remote_socket_started = 1;
			}
		}
	}
	if (control_head_data_width > n_pixels) {
		n_pixels = control_head_data_width;
		if (pixels)
			free(pixels);
		pixels = (double *)malloc(n_pixels * sizeof(double));
	}
	copy2pixels(pixels, control_head_data_width, fft_avg, fft_size, zoom, deltaf, fft_sample_rate);
	// Send multiple 16-bit data blocks: {flags, sequence}, block number, 16-bit graph data
	// 8-bit flags:
	//	bit 0: clip indicator
	// 8-bit sequence: 0, 1, 2, ..., 255
	block = 0;
	pixel_index = 0;
	while (pixel_index < control_head_data_width) {
		if (quisk_get_overrange())
			flags = 0x01;
		else
			flags = 0x00;
		buffer[0] = flags << 8 | sequence;
		buffer[1] = block;
		buffer_index = 2;
		while (buffer_index < GRAPH_DATA_BLOCK && pixel_index < control_head_data_width) {
			d1 = pixels[pixel_index++];
			if (fabs(d1) < 1e-40)	// avoid log10(0)
				d1 = 1E-40;
			d2 = 20.0 * log10(d1) - scale;
			if (d2 < -200)
				d2 = -200;
			else if (d2 > 0)
				d2 = 0;
			buffer[buffer_index++] = (int16_t)lround(d2 * GRAPH_DATA_SCALE);
		}
		sent = send(graph_data_to_control_head_socket, (const char *)buffer, buffer_index * 2, 0);
                //     	  	(const struct sockaddr *)&AddrControlHeadGraph, sizeof(AddrControlHeadGraph));
		if (sent != buffer_index * 2)
			QuiskPrintf("send_graph_data(), send(): %s\n", strerror(errno));
		block++;
	}
	sequence += 1;
}

int receive_graph_data(double * fft_avg)
{  // called by the sound thread
	int i, i1, i2;
	ssize_t count;
	uint8_t seq, flags;
	int16_t buffer[GRAPH_DATA_BLOCK];
	int16_t block;
	static int16_t * pixels = NULL;
	static int n_pixels = 0;
	static int total = 0;
	static int16_t sequence = 0;

	if (graph_data_from_remote_radio_socket == INVALID_SOCKET)
		return 0;
	// Signal far end (server) that we're ready (this sends our address/port to far end)
	if ( !graph_from_remote_socket_started) {
		i = send(graph_data_from_remote_radio_socket, "rr\n", 3, 0);
		if (i != 3)
			QuiskPrintf("receive_graph_data(), send(): %s\n", strerror(errno));
	}
	if (n_pixels < data_width) {
		n_pixels = data_width;
		if (pixels)
			free(pixels);
		pixels = (int16_t *)malloc(n_pixels * sizeof(int16_t));
	}
	count = recv(graph_data_from_remote_radio_socket, (char *)buffer, GRAPH_DATA_BLOCK * 2, 0);
	count /= 2;	// convert to int16_t
	if (count > 2) {
		graph_from_remote_socket_started = 1;
		flags = buffer[0] >> 8;
		if (flags & 0x01)	// Clip
			quisk_sound_state.overrange++;
		seq = buffer[0] & 0xFF;
		if (seq != sequence) {	// new graph data
			sequence = seq;
			total = 0;
		}
		block = buffer[1];
		count -= 2;	// number of 16-bit graph data items
		i1 = block * (GRAPH_DATA_BLOCK - 2);
		i2 = i1 + count;
		if (i1 >= 0 && i2 <= data_width) {
			memcpy(pixels + i1, buffer + 2, count * 2);
			total += count;
			if (total == data_width) {
				for (i = 0; i < data_width; i++)
					fft_avg[i] = (double)pixels[i] / GRAPH_DATA_SCALE;
				return data_width;
			}
		}
	}
	return 0;
}


static int start_winsock()
{
#ifdef MS_WINDOWS
	WORD wVersionRequested = MAKEWORD(2, 2);
	WSADATA wsaData;

	if (WSAStartup(wVersionRequested, &wsaData) != 0) {
		QuiskPrintf("start_winsock(): %s\n", strerror(errno));
		return 0;		// failure to start winsock
	}
#endif
	return 1;
}





static void open_remote_sound_server(SOCKET * sock, char * ip, int port, int sndsize, char * name, int non_block)
{
	struct sockaddr_in bind_addr;
	const char enable = 1;	// for sockopt
#ifndef MS_WINDOWS
	int tos = 184;	// DSCP "Expedite" (46)
#endif

	if (!start_winsock()) {
		QuiskPrintf("open_remote_sound_server for %s: Failure to start WinSock\n", name);
		return;
	}

	*sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (*sock != INVALID_SOCKET) {
		setsockopt(*sock, SOL_SOCKET, SO_SNDBUF, (char *)&sndsize, sizeof(sndsize));
		setsockopt(*sock, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable));
#ifndef MS_WINDOWS
		setsockopt(*sock, IPPROTO_IP, IP_TOS, &tos, sizeof(tos));
#endif

		// bind to this computer for receiving (and reading far-end address from client)
		memset((char *) &bind_addr, 0, sizeof(bind_addr));
		bind_addr.sin_family = AF_INET;
		bind_addr.sin_port = htons(port);
		bind_addr.sin_addr.s_addr = htonl(INADDR_ANY);
		if (bind(*sock, (const struct sockaddr *)&bind_addr, sizeof(bind_addr)) != 0) {
			QuiskPrintf("open_remote_sound_server(), bind(): %s\n", strerror(errno));
			close(*sock);
			*sock = INVALID_SOCKET;
		}
		else if (non_block) {
#ifdef MS_WINDOWS
       			unsigned long one = 1;
			ioctlsocket(*sock, FIONBIO, &one);	// set non-blocking
#else
			int flags;
			flags = fcntl(*sock, F_GETFL, 0);	// set non-blocking
			fcntl(*sock, F_SETFL, flags | O_NONBLOCK);
#endif
		}
	}
	if (*sock == INVALID_SOCKET) {
		QuiskPrintf("open server %s: Failure to open socket\n", name);
	}
	else {
		QuiskPrintf("open server %s: opened socket %s port %i\n", name, ip, port);
	}
}


static void open_remote_sound_client(SOCKET * sock, char * ip, int port, int sndsize, char * name, int non_block)
{
	struct sockaddr_in Addr;
	const char enable = 1;	// for sockopt

	if (!start_winsock()) {
		QuiskPrintf("open_remote_sound_client for %s: Failure to start WinSock\n", name);
		return;
	}

	*sock = socket(PF_INET, SOCK_DGRAM, 0);
	if (*sock != INVALID_SOCKET) {
		setsockopt(*sock, SOL_SOCKET, SO_RCVBUF, (char *)&sndsize, sizeof(sndsize));
		setsockopt(*sock, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(enable));

		// set far-end address structure to enable sending initial packet to get things started
		Addr.sin_family = AF_INET;
		Addr.sin_port = htons(port);
#ifdef MS_WINDOWS
		Addr.sin_addr.S_un.S_addr = inet_addr(ip);
#else
		inet_aton(ip, &Addr.sin_addr);
#endif
		if (connect(*sock, (const struct sockaddr *)&Addr, sizeof(Addr)) != 0) {
			close(*sock);
			*sock = INVALID_SOCKET;
		}
		else if (non_block) {
#ifdef MS_WINDOWS
       			unsigned long one = 1;
			ioctlsocket(*sock, FIONBIO, &one);	// set non-blocking
#else
			int flags;
			flags = fcntl(*sock, F_GETFL, 0);	// set non-blocking
			fcntl(*sock, F_SETFL, flags | O_NONBLOCK);
#endif
		}
	}
	if (*sock == INVALID_SOCKET) {
		QuiskPrintf("open client %s: Failure to open socket\n", name);
	}
	else {
		QuiskPrintf("open client %s: opened socket %s port %i\n", name, ip, port);
	}
}


static void close_remote_sound_socket(SOCKET * sock, char * name)
{
	if (*sock != INVALID_SOCKET) {
		close(*sock);
		*sock = INVALID_SOCKET;
#ifdef MS_WINDOWS
		WSACleanup();
#endif
		QuiskPrintf("%s: closed socket\n", name);
	}
	else {
		QuiskPrintf("%s: socket already closed\n", name);
	}
}

// start running UDP remote sound on control_head ...
// ... receive radio sound from remote_radio, send mic sound to remote_radio
PyObject * quisk_start_control_head_remote_sound(PyObject * self, PyObject * args)
{
	int radio_sound_port;
	int mic_sound_port;
	int graph_data_port;
	int sndsize = 48000;
	char * remote_radio_ip;	// IP address of far end
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, "siii", &remote_radio_ip, &radio_sound_port, &mic_sound_port, &graph_data_port))
		return NULL;

	name = "radio sound from remote_radio";
	sock = &radio_sound_from_remote_radio_socket;
	open_remote_sound_client(sock, remote_radio_ip, radio_sound_port, sndsize, name, 0);

	name = "mic sound to remote radio";
	sock = &mic_sound_to_remote_radio_socket;
	open_remote_sound_server(sock, remote_radio_ip, mic_sound_port, sndsize, name, 0);

	name = "graph data from remote_radio";
	sock = &graph_data_from_remote_radio_socket;
	open_remote_sound_client(sock, remote_radio_ip, graph_data_port, 1024 * 8, name, 1);

	packets_sent = 0;
	packets_recd = 0;

	return Py_None;
}

// stop running UDP remote sound on control_head
PyObject * quisk_stop_control_head_remote_sound(PyObject * self, PyObject * args)
{
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, ""))
		return NULL;

	name = "radio sound from remote_radio";
	sock = &radio_sound_from_remote_radio_socket;
	close_remote_sound_socket(sock, name);

	name = "mic sound to remote radio";
	sock = &mic_sound_to_remote_radio_socket;
	close_remote_sound_socket(sock, name);

	name = "graph data from remote_radio";
	sock = &graph_data_from_remote_radio_socket;
	close_remote_sound_socket(sock, name);

	sound_from_remote_socket_started = 0;	// reset for next time
	sound_to_remote_socket_started = 0;
	graph_from_remote_socket_started = 0;
	graph_to_remote_socket_started = 0;

	QuiskPrintf("total packets sent = %i, recd = %i\n", packets_sent, packets_recd);

	return Py_None;
}

// start running UDP remote sound on remote_radio ...
// ... send radio sound to control_head, receive mic sound from control_head
PyObject * quisk_start_remote_radio_remote_sound(PyObject * self, PyObject * args)
{
	int radio_sound_port;
	int mic_sound_port;
	int graph_data_port;
	int sndsize = 48000;
	char * control_head_ip;	// IP address of far end
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, "siiii", &control_head_ip, &radio_sound_port, &mic_sound_port,
                     &graph_data_port, &control_head_data_width))
		return NULL;

	//memset((char *) &AddrControlHeadGraph, 0, sizeof(AddrControlHeadGraph));
	//AddrControlHeadGraph.sin_family = AF_INET;
	//AddrControlHeadGraph.sin_port = htons(graph_data_port);
#ifdef MS_WINDOWS
	//AddrControlHeadGraph.sin_addr.S_un.S_addr = inet_addr(control_head_ip);
#else
	//inet_aton(control_head_ip, &AddrControlHeadGraph.sin_addr);
#endif

	name = "radio sound to control_head";
	sock = &radio_sound_to_control_head_socket;
	open_remote_sound_server(sock, control_head_ip, radio_sound_port, sndsize, name, 0);

	name = "mic sound from control_head";
	sock = &mic_sound_from_control_head_socket;
	open_remote_sound_client(sock, control_head_ip, mic_sound_port, sndsize, name, 0);

	name = "graph data to control_head";
	sock = &graph_data_to_control_head_socket;
	open_remote_sound_server(sock, control_head_ip, graph_data_port, 1024 * 8, name, 1);

	packets_sent = 0;
	packets_recd = 0;

	return Py_None;
}

// stop running UDP remote sound on remote_radio
PyObject * quisk_stop_remote_radio_remote_sound(PyObject * self, PyObject * args)
{
	char * name;
	SOCKET * sock;

	if (!PyArg_ParseTuple (args, ""))
		return NULL;

	name = "radio sound to control_head";
	sock = &radio_sound_to_control_head_socket;
	close_remote_sound_socket(sock, name);

	name = "mic sound from control_head";
	sock = &mic_sound_from_control_head_socket;
	close_remote_sound_socket(sock, name);

	name = "graph data to control_head";
	sock = &graph_data_to_control_head_socket;
	close_remote_sound_socket(sock, name);

	sound_from_remote_socket_started = 0;	// reset for next time
	sound_to_remote_socket_started = 0;
	graph_from_remote_socket_started = 0;
	graph_to_remote_socket_started = 0;
	control_head_data_width = 0;

	QuiskPrintf("total packets sent = %i, recd = %i\n", packets_sent, packets_recd);

	return Py_None;
}
