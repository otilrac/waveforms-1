#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: MGS Rocksat Receiver v1.0
# Generated: Tue May 23 01:43:01 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import burst
import es
import kiss
import mapper
import pmt,struct,numpy,math
import pyqt
import sip
import sys
import time
from gnuradio import qtgui


class mgs_rx_hdlc_1(gr.top_block, Qt.QWidget):

    def __init__(self, ip='127.0.0.1', iq_file='./rocksat_125kbd_500ksps_date_comment.dat', meta_rate=.1, port='52001', pre_bits=[0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0], record_iq=0, record_rfo=0, record_snr=0, rfo_file='./rocksat_rfo_date_comment.meta', snr_file='./rocksat_snr_date_comment.meta'):
        gr.top_block.__init__(self, "MGS Rocksat Receiver v1.0")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("MGS Rocksat Receiver v1.0")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "mgs_rx_hdlc_1")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.ip = ip
        self.iq_file = iq_file
        self.meta_rate = meta_rate
        self.port = port
        self.pre_bits = pre_bits
        self.record_iq = record_iq
        self.record_rfo = record_rfo
        self.record_snr = record_snr
        self.rfo_file = rfo_file
        self.snr_file = snr_file

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 500e3
        self.baud = baud = 125e3
        self.samps_per_symb = samps_per_symb = int(samp_rate/baud)
        self.rx_offset = rx_offset = 250e3
        self.rx_gain = rx_gain = 25
        self.rx_freq = rx_freq = 2395e6
        self.mult = mult = (samp_rate)/2/3.141593

        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, samp_rate, samp_rate/2, 1000, firdes.WIN_HAMMING, 6.76)

        self.lo = lo = 1833e6
        self.khz_offset = khz_offset = 0
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_range = Range(0, 86, 1, 25, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 0,8,1,4)
        self._khz_offset_range = Range(-150, 150, 1, 0, 200)
        self._khz_offset_win = RangeWidget(self._khz_offset_range, self.set_khz_offset, 'Offset [kHz]', "counter_slider", float)
        self.top_grid_layout.addWidget(self._khz_offset_win, 1,8,1,4)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq, rx_offset), 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'', #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.010)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['pre-d', 'post', '', '', '',
                  '', '', '', '', '']
        colors = [0, 1, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-130, -60)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 8,0,8,8)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024*4, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate , #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.0010)
        self.qtgui_freq_sink_x_0.set_y_axis(-120, -20)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['pre-d', 'post', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,8,8)
        self.pyqt_trim_tail_0 = pyqt.trim_tail(20)
        self.pyqt_time_plot_1_0_0 = pyqt.time_plot('Soft Bits')
        self._pyqt_time_plot_1_0_0_win = self.pyqt_time_plot_1_0_0;
        self.top_grid_layout.addWidget(self._pyqt_time_plot_1_0_0_win, 4,8,1,4)
        self.pyqt_time_plot_1_0 = pyqt.time_plot('Hard Bits')
        self._pyqt_time_plot_1_0_win = self.pyqt_time_plot_1_0;
        self.top_grid_layout.addWidget(self._pyqt_time_plot_1_0_win, 5,8,1,4)
        self.pyqt_text_output_0 = pyqt.text_output()
        self._pyqt_text_output_0_win = self.pyqt_text_output_0;
        self.top_grid_layout.addWidget(self._pyqt_text_output_0_win, 6,8,4,4)
        self.pyqt_skip_head_0 = pyqt.skip_head(100)
        self.pyqt_head_0 = pyqt.head(1024)
        self.pyqt_cpower_plot_0_0 = pyqt.cpower_plot('Burst Post Length-D')
        self._pyqt_cpower_plot_0_0_win = self.pyqt_cpower_plot_0_0;
        self.top_grid_layout.addWidget(self._pyqt_cpower_plot_0_0_win, 2,8,1,4)
        self.pyqt_const_plot_0_0 = pyqt.const_plot(label='Symbols')
        self._pyqt_const_plot_0_0_win = self.pyqt_const_plot_0_0;
        self.top_grid_layout.addWidget(self._pyqt_const_plot_0_0_win, 3,8,1,4)
        self.mapper_demapper_soft_0 = mapper.demapper_soft(mapper.BPSK, ([0,1]))
        self.mapper_demapper_msg_0_0 = mapper.demapper_msg(mapper.BPSK, ([0,1]))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, (baud *(1+alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))
        self.kiss_nrzi_decode_0 = kiss.nrzi_decode()
        self.kiss_hdlc_deframer_0 = kiss.hdlc_deframer(check_fcs=True, max_length=1024)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (lpf_taps), khz_offset*1000, samp_rate)
        self.es_trigger_edge_f_0 = es.trigger_edge_f(-1,256*16,100,gr.sizeof_gr_complex,500)
        self.es_sink_0 = es.sink(1*[gr.sizeof_gr_complex],4,128,0,2,0)
        self.es_handler_pdu_0 = es.es_make_handler_pdu(es.es_handler_print.TYPE_C32)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(math.pi*2/100, 2, False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(math.pi*2/100, 2, False)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_cc(samps_per_symb*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.burst_slicer_0 = burst.slicer()
        self.burst_preamble_correlator_0 = burst.preamble_correlator(4, 0.5, (pre_bits))
        self.burst_length_detect_c_0 = burst.length_detect_c()
        (self.burst_length_detect_c_0).set_min_output_buffer(20800)
        self.burst_correlator_filter_0 = burst.correlator_filter(100, 1e-4, -10)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", ip, port, 1024, False)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.complex_t, 'pl2')
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((10, ))
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_agc2_xx_0_0 = analog.agc2_cc(1e-3, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.mapper_demapper_msg_0_0, 'cpdus'))
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.pyqt_const_plot_0_0, 'cpdus'))
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.pyqt_cpower_plot_0_0, 'cpdus'))
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.pyqt_trim_tail_0, 'pdus'))
        self.msg_connect((self.burst_slicer_0, 'pdus'), (self.pyqt_time_plot_1_0, 'pdus'))
        self.msg_connect((self.es_handler_pdu_0, 'pdus_out'), (self.burst_length_detect_c_0, 'cpdus'))
        self.msg_connect((self.es_trigger_edge_f_0, 'edge_event'), (self.es_handler_pdu_0, 'handle_event'))
        self.msg_connect((self.es_trigger_edge_f_0, 'which_stream'), (self.es_sink_0, 'schedule_event'))
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.pyqt_text_output_0, 'pdus'))
        self.msg_connect((self.mapper_demapper_msg_0_0, 'fpdus'), (self.burst_slicer_0, 'fpdus'))
        self.msg_connect((self.mapper_demapper_msg_0_0, 'fpdus'), (self.pyqt_time_plot_1_0_0, 'pdus'))
        self.msg_connect((self.pyqt_head_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.pyqt_skip_head_0, 'pdus'), (self.pyqt_head_0, 'pdus'))
        self.msg_connect((self.pyqt_trim_tail_0, 'pdus'), (self.pyqt_skip_head_0, 'pdus'))
        self.connect((self.analog_agc2_xx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.burst_correlator_filter_0, 0), (self.es_trigger_edge_f_0, 0))
        self.connect((self.burst_preamble_correlator_0, 0), (self.burst_correlator_filter_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.burst_preamble_correlator_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.es_trigger_edge_f_0, 1))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.mapper_demapper_soft_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.kiss_nrzi_decode_0, 0))
        self.connect((self.es_trigger_edge_f_0, 0), (self.es_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc2_xx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.kiss_nrzi_decode_0, 0), (self.kiss_hdlc_deframer_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.mapper_demapper_soft_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mgs_rx_hdlc_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_iq_file(self):
        return self.iq_file

    def set_iq_file(self, iq_file):
        self.iq_file = iq_file

    def get_meta_rate(self):
        return self.meta_rate

    def set_meta_rate(self, meta_rate):
        self.meta_rate = meta_rate

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_pre_bits(self):
        return self.pre_bits

    def set_pre_bits(self, pre_bits):
        self.pre_bits = pre_bits

    def get_record_iq(self):
        return self.record_iq

    def set_record_iq(self, record_iq):
        self.record_iq = record_iq

    def get_record_rfo(self):
        return self.record_rfo

    def set_record_rfo(self, record_rfo):
        self.record_rfo = record_rfo

    def get_record_snr(self):
        return self.record_snr

    def set_record_snr(self, record_snr):
        self.record_snr = record_snr

    def get_rfo_file(self):
        return self.rfo_file

    def set_rfo_file(self, rfo_file):
        self.rfo_file = rfo_file

    def get_snr_file(self):
        return self.snr_file

    def set_snr_file(self, snr_file):
        self.snr_file = snr_file

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samps_per_symb(int(self.samp_rate/self.baud))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate )
        self.set_mult((self.samp_rate)/2/3.141593)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.baud *(1+self.alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samps_per_symb(int(self.samp_rate/self.baud))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.baud *(1+self.alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samps_per_symb*(1+0.0))

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.rx_offset), 0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)


    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq, self.rx_offset), 0)

    def get_mult(self):
        return self.mult

    def set_mult(self, mult):
        self.mult = mult

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.lpf_taps))

    def get_lo(self):
        return self.lo

    def set_lo(self, lo):
        self.lo = lo

    def get_khz_offset(self):
        return self.khz_offset

    def set_khz_offset(self, khz_offset):
        self.khz_offset = khz_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.khz_offset*1000)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.baud *(1+self.alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-a", "--ip", dest="ip", type="string", default='127.0.0.1',
        help="Set 127.0.0.1 [default=%default]")
    parser.add_option(
        "", "--iq-file", dest="iq_file", type="string", default='./rocksat_125kbd_500ksps_date_comment.dat',
        help="Set iq_file [default=%default]")
    parser.add_option(
        "", "--meta-rate", dest="meta_rate", type="eng_float", default=eng_notation.num_to_str(.1),
        help="Set meta_rate [default=%default]")
    parser.add_option(
        "-p", "--port", dest="port", type="string", default='52001',
        help="Set 52001 [default=%default]")
    parser.add_option(
        "", "--record-iq", dest="record_iq", type="intx", default=0,
        help="Set record_iq [default=%default]")
    parser.add_option(
        "", "--record-rfo", dest="record_rfo", type="intx", default=0,
        help="Set record_rfo [default=%default]")
    parser.add_option(
        "", "--record-snr", dest="record_snr", type="intx", default=0,
        help="Set record_snr [default=%default]")
    parser.add_option(
        "", "--rfo-file", dest="rfo_file", type="string", default='./rocksat_rfo_date_comment.meta',
        help="Set rfo_file [default=%default]")
    parser.add_option(
        "", "--snr-file", dest="snr_file", type="string", default='./rocksat_snr_date_comment.meta',
        help="Set snr_file [default=%default]")
    return parser


def main(top_block_cls=mgs_rx_hdlc_1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ip=options.ip, iq_file=options.iq_file, meta_rate=options.meta_rate, port=options.port, record_iq=options.record_iq, record_rfo=options.record_rfo, record_snr=options.record_snr, rfo_file=options.rfo_file, snr_file=options.snr_file)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
