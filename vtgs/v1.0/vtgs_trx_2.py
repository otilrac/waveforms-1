#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: VTGS Rocksat-X 2017 Transceiver v2.0
# Generated: Sat Aug  5 13:50:31 2017
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
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import kiss
import mapper
import pmt,struct,numpy,math ; from datetime import datetime as dt; import string
import pyqt
import sip
import sys
import time
import vtgs
from gnuradio import qtgui


class vtgs_trx_2(gr.top_block, Qt.QWidget):

    def __init__(self, gs_name='VTGS', ip='0.0.0.0', iq_file='./rocksat_125kbd_500ksps_date_comment.dat', meta_rate=.1, port='52001', record_iq=0, record_rfo=0, record_snr=0, rfo_file='./rocksat_rfo_date_comment.meta', snr_file='./rocksat_snr_date_comment.meta', tx_freq=1265e6, tx_offset=250e3):
        gr.top_block.__init__(self, "VTGS Rocksat-X 2017 Transceiver v2.0")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("VTGS Rocksat-X 2017 Transceiver v2.0")
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

        self.settings = Qt.QSettings("GNU Radio", "vtgs_trx_2")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.gs_name = gs_name
        self.ip = ip
        self.iq_file = iq_file
        self.meta_rate = meta_rate
        self.port = port
        self.record_iq = record_iq
        self.record_rfo = record_rfo
        self.record_snr = record_snr
        self.rfo_file = rfo_file
        self.snr_file = snr_file
        self.tx_freq = tx_freq
        self.tx_offset = tx_offset

        ##################################################
        # Variables
        ##################################################
        self.ts_str = ts_str = dt.strftime(dt.utcnow(), "%Y%m%d_%H%M%S.%f" )+'_UTC'
        self.samp_rate = samp_rate = 500e3
        self.baud = baud = 125e3
        self.samps_per_symb = samps_per_symb = int(samp_rate/baud)
        self.rx_freq = rx_freq = 2395e6
        self.iq_fn = iq_fn = "{:s}_{:s}_{:s}k.fc32".format(gs_name, ts_str, str(int(samp_rate)/1000))
        self.alpha = alpha = 0.5
        self.uplink_label = uplink_label = ''
        self.tx_gain = tx_gain = 25
        self.tx_correct = tx_correct = 2000
        self.rx_offset = rx_offset = 250e3
        self.rx_gain = rx_gain = 1
        self.rx_freq_lbl = rx_freq_lbl = "{:4.3f}".format(rx_freq/1e6)

        self.rrc_filter_taps = rrc_filter_taps = firdes.root_raised_cosine(32, 1.0, 1.0/(samps_per_symb*32), alpha, samps_per_symb*32)

        self.mult = mult = (samp_rate)/2/3.141593

        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, samp_rate, samp_rate/2, 1000, firdes.WIN_HAMMING, 6.76)

        self.lo = lo = 1833e6
        self.khz_offset = khz_offset = 0
        self.iq_fp = iq_fp = "/captures/rocksat/{:s}".format(iq_fn)
        self.bb_gain = bb_gain = .75

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 86, 1, 25, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_win, 10,8,1,4)
        self._tx_correct_range = Range(-10000, 10000, 1, 2000, 200)
        self._tx_correct_win = RangeWidget(self._tx_correct_range, self.set_tx_correct, "tx_correct", "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_correct_win, 12,8,1,4)
        self._rx_gain_range = Range(0, 86, 1, 1, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 3,8,1,4)
        self._khz_offset_range = Range(-150, 150, 1, 0, 200)
        self._khz_offset_win = RangeWidget(self._khz_offset_range, self.set_khz_offset, 'Offset [kHz]', "counter_slider", float)
        self.top_grid_layout.addWidget(self._khz_offset_win, 4,8,1,4)
        self._bb_gain_range = Range(0, 1, .01, .75, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, 'bb_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._bb_gain_win, 11,8,1,4)
        self.vtgs_mult_descrambler_0 = vtgs.mult_descrambler(17, 0x3FFFF)
        self.vtgs_ao40_decoder_0_0 = vtgs.ao40_decoder()
        self._uplink_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._uplink_label_formatter = None
        else:
          self._uplink_label_formatter = lambda x: str(x)

        self._uplink_label_tool_bar.addWidget(Qt.QLabel('TX MSG'+": "))
        self._uplink_label_label = Qt.QLabel(str(self._uplink_label_formatter(self.uplink_label)))
        self._uplink_label_tool_bar.addWidget(self._uplink_label_label)
        self.top_grid_layout.addWidget(self._uplink_label_tool_bar, 9,8,1,1)

        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(rx_freq-lo, rx_offset), 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(tx_freq+tx_correct, tx_offset), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self._rx_freq_lbl_tool_bar = Qt.QToolBar(self)

        if None:
          self._rx_freq_lbl_formatter = None
        else:
          self._rx_freq_lbl_formatter = lambda x: str(x)

        self._rx_freq_lbl_tool_bar.addWidget(Qt.QLabel('RX Freq [MHz]'+": "))
        self._rx_freq_lbl_label = Qt.QLabel(str(self._rx_freq_lbl_formatter(self.rx_freq_lbl)))
        self._rx_freq_lbl_tool_bar.addWidget(self._rx_freq_lbl_label)
        self.top_grid_layout.addWidget(self._rx_freq_lbl_tool_bar, 0,10,1,2)

        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=10,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=8,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=8,
                taps=None,
                fractional_bw=None,
        )
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

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-130, -20)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 5,0,4,8)
        self.qtgui_number_sink_2 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_2.set_update_time(0.10)
        self.qtgui_number_sink_2.set_title("")

        labels = ['EVM', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_2.set_min(i, -1)
            self.qtgui_number_sink_2.set_max(i, 1)
            self.qtgui_number_sink_2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_2.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_2.set_label(i, labels[i])
            self.qtgui_number_sink_2.set_unit(i, units[i])
            self.qtgui_number_sink_2.set_factor(i, factor[i])

        self.qtgui_number_sink_2.enable_autoscale(False)
        self._qtgui_number_sink_2_win = sip.wrapinstance(self.qtgui_number_sink_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_2_win, 2,8,1,4)
        self.qtgui_number_sink_0_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0_0.set_title("")

        labels = ['SNR', '', '', '', '',
                  '', '', '', '', '']
        units = ['dB', '', '', '', '',
                 '', '', '', '', '']
        colors = [("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_0_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_0_0_0.set_max(i, 30)
            self.qtgui_number_sink_0_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_0_0_0_win, 1,8,1,4)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['RX Freq Offset', 'SNR', '', '', '',
                  '', '', '', '', '']
        units = ['Hz', 'dB', '', '', '',
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
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 0,8,1,2)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/10, #bw
        	"TX Spectrum", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(True)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 9,0,4,8)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024*4, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate , #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.0010)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, -20)
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,5,8)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
        	1024, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-1, 1)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 5,8,4,4)
        self.pyqt_text_input_0 = pyqt.text_input()
        self._pyqt_text_input_0_win = self.pyqt_text_input_0;
        self.top_grid_layout.addWidget(self._pyqt_text_input_0_win, 9,9,1,3)
        self.mapper_demapper_soft_0 = mapper.demapper_soft(mapper.BPSK, ([0,1]))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, (baud *(1+alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))
        self.kiss_hdlc_framer_0 = kiss.hdlc_framer(preamble_bytes=64, postamble_bytes=16)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (lpf_taps), khz_offset*1000, samp_rate)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x0, 16)
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(samps_per_symb, math.pi*2/100, (rrc_filter_taps), 32, 16, 1.5, 1)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=50,
        	bt=alpha,
        	verbose=False,
        	log=False,
        )
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(math.pi*2/100, 2, False)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(math.pi*2/100, 2, False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_socket_pdu_0_2 = blocks.socket_pdu("UDP_SERVER", ip, '52002', 1024, False)
        self.blocks_socket_pdu_0_1 = blocks.socket_pdu("TCP_SERVER", ip, '52003', 1024, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_CLIENT", ip, port, 1024, False)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_nlog10_ff_0_1 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((bb_gain, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((mult, ))
        self.blocks_moving_average_xx_0_0_1 = blocks.moving_average_ff(100000, 0.00001, 4000)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(1000, 0.001, 4000)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(100000, 0.00001, 4000)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, iq_fp, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=2,
        	input_index=0,
        	output_index=int(record_iq),
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 125e3, 1, 0)
        self.analog_agc2_xx_0_0 = analog.agc2_cc(1e-3, 1e-2, 1.0, 1.0)
        self.analog_agc2_xx_0_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_1, 'pdus'), (self.kiss_hdlc_framer_0, 'in'))
        self.msg_connect((self.blocks_socket_pdu_0_2, 'pdus'), (self.kiss_hdlc_framer_0, 'in'))
        self.msg_connect((self.kiss_hdlc_framer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.pyqt_text_input_0, 'pdus'), (self.kiss_hdlc_framer_0, 'in'))
        self.msg_connect((self.vtgs_ao40_decoder_0_0, 'valid_frames'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.vtgs_ao40_decoder_0_0, 'valid_frames'), (self.blocks_socket_pdu_0_1, 'pdus'))
        self.connect((self.analog_agc2_xx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blks2_selector_0, 1), (self.blocks_file_sink_0, 0))
        self.connect((self.blks2_selector_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_number_sink_2, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_nlog10_ff_0_1, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_1, 0), (self.qtgui_number_sink_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_nlog10_ff_0_1, 0), (self.blocks_moving_average_xx_0_0_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.mapper_demapper_soft_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 1), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.vtgs_mult_descrambler_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_agc2_xx_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.mapper_demapper_soft_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.rational_resampler_xxx_2, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blks2_selector_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.vtgs_mult_descrambler_0, 0), (self.vtgs_ao40_decoder_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "vtgs_trx_2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_gs_name(self):
        return self.gs_name

    def set_gs_name(self, gs_name):
        self.gs_name = gs_name
        self.set_iq_fn("{:s}_{:s}_{:s}k.fc32".format(self.gs_name, self.ts_str, str(int(self.samp_rate)/1000)))

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

    def get_record_iq(self):
        return self.record_iq

    def set_record_iq(self, record_iq):
        self.record_iq = record_iq
        self.blks2_selector_0.set_output_index(int(int(self.record_iq)))

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

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_ts_str(self):
        return self.ts_str

    def set_ts_str(self, ts_str):
        self.ts_str = ts_str
        self.set_iq_fn("{:s}_{:s}_{:s}k.fc32".format(self.gs_name, self.ts_str, str(int(self.samp_rate)/1000)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samps_per_symb(int(self.samp_rate/self.baud))
        self.set_mult((self.samp_rate)/2/3.141593)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate/10)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate )
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.baud *(1+self.alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))
        self.set_iq_fn("{:s}_{:s}_{:s}k.fc32".format(self.gs_name, self.ts_str, str(int(self.samp_rate)/1000)))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

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

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq-self.lo, self.rx_offset), 0)
        self.set_rx_freq_lbl(self._rx_freq_lbl_formatter("{:4.3f}".format(self.rx_freq/1e6)))

    def get_iq_fn(self):
        return self.iq_fn

    def set_iq_fn(self, iq_fn):
        self.iq_fn = iq_fn
        self.set_iq_fp("/captures/rocksat/{:s}".format(self.iq_fn))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.baud *(1+self.alpha) )/2, 1000, firdes.WIN_HAMMING, 6.76))

    def get_uplink_label(self):
        return self.uplink_label

    def set_uplink_label(self, uplink_label):
        self.uplink_label = uplink_label
        Qt.QMetaObject.invokeMethod(self._uplink_label_label, "setText", Qt.Q_ARG("QString", self.uplink_label))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)


    def get_tx_correct(self):
        return self.tx_correct

    def set_tx_correct(self, tx_correct):
        self.tx_correct = tx_correct
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq-self.lo, self.rx_offset), 0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)


    def get_rx_freq_lbl(self):
        return self.rx_freq_lbl

    def set_rx_freq_lbl(self, rx_freq_lbl):
        self.rx_freq_lbl = rx_freq_lbl
        Qt.QMetaObject.invokeMethod(self._rx_freq_lbl_label, "setText", Qt.Q_ARG("QString", self.rx_freq_lbl))

    def get_rrc_filter_taps(self):
        return self.rrc_filter_taps

    def set_rrc_filter_taps(self, rrc_filter_taps):
        self.rrc_filter_taps = rrc_filter_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps((self.rrc_filter_taps))

    def get_mult(self):
        return self.mult

    def set_mult(self, mult):
        self.mult = mult
        self.blocks_multiply_const_vxx_0.set_k((self.mult, ))

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.lpf_taps))

    def get_lo(self):
        return self.lo

    def set_lo(self, lo):
        self.lo = lo
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.rx_freq-self.lo, self.rx_offset), 0)

    def get_khz_offset(self):
        return self.khz_offset

    def set_khz_offset(self, khz_offset):
        self.khz_offset = khz_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.khz_offset*1000)

    def get_iq_fp(self):
        return self.iq_fp

    def set_iq_fp(self, iq_fp):
        self.iq_fp = iq_fp
        self.blocks_file_sink_0.open(self.iq_fp)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.bb_gain, ))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--gs-name", dest="gs_name", type="string", default='VTGS',
        help="Set gs_name [default=%default]")
    parser.add_option(
        "-a", "--ip", dest="ip", type="string", default='0.0.0.0',
        help="Set 0.0.0.0 [default=%default]")
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
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(1265e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(250e3),
        help="Set tx_offset [default=%default]")
    return parser


def main(top_block_cls=vtgs_trx_2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(gs_name=options.gs_name, ip=options.ip, iq_file=options.iq_file, meta_rate=options.meta_rate, port=options.port, record_iq=options.record_iq, record_rfo=options.record_rfo, record_snr=options.record_snr, rfo_file=options.rfo_file, snr_file=options.snr_file, tx_freq=options.tx_freq, tx_offset=options.tx_offset)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
