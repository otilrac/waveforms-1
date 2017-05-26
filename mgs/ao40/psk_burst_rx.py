#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Psk Burst Rx
# Generated: Tue May 23 02:12:26 2017
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
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import burst
import es
import pmt,struct,numpy,math
import pyqt
import sip
import sys
import time
from gnuradio import qtgui


class psk_burst_rx(gr.top_block, Qt.QWidget):

    def __init__(self, pre_bits=[1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,1,1,1,1,0,0,1,0,1,1,0,0,1,0,0,
1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,1,0,1,1,0,1,1,0,0,0]):
        gr.top_block.__init__(self, "Psk Burst Rx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Psk Burst Rx")
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

        self.settings = Qt.QSettings("GNU Radio", "psk_burst_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.pre_bits = pre_bits

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 500e3
        self.baud = baud = 125e3
        self.samps_per_symb = samps_per_symb = int(samp_rate/baud)
        self.alpha = alpha = 0.5
        self.rx_offset = rx_offset = 250e3
        self.rx_gain = rx_gain = 25
        self.rx_freq = rx_freq = 2395e6

        self.rrc_filter_taps = rrc_filter_taps = firdes.root_raised_cosine(32, 1.0, 1.0/(samps_per_symb*32), alpha, samps_per_symb*32)


        ##################################################
        # Blocks
        ##################################################
        self._rx_gain_range = Range(0, 86, 1, 25, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, 'RX Gain', "counter_slider", float)
        self.top_layout.addWidget(self._rx_gain_win)
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
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	8192, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-10, 10)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 1,0,1,2)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	8192, #size
        	samp_rate, #samp_rate
        	'', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-.01, .01)

        self.qtgui_time_sink_x_0.set_y_label('', '')

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0,0,1,2)
        self.pyqt_cpower_plot_0_0 = pyqt.cpower_plot('Burst Post Length-D')
        self._pyqt_cpower_plot_0_0_win = self.pyqt_cpower_plot_0_0;
        self.top_grid_layout.addWidget(self._pyqt_cpower_plot_0_0_win, 2,1,1,1)
        self.pyqt_const_plot_0 = pyqt.const_plot(label='Pre-Sync Syms')
        self._pyqt_const_plot_0_win = self.pyqt_const_plot_0;
        self.top_grid_layout.addWidget(self._pyqt_const_plot_0_win, 3,0,1,1)
        self.es_trigger_edge_f_0 = es.trigger_edge_f(5,5200*4,100,gr.sizeof_gr_complex,500)
        self.es_sink_0 = es.sink(1*[gr.sizeof_gr_complex],4,128,0,2,0)
        self.es_handler_pdu_0 = es.es_make_handler_pdu(es.es_handler_print.TYPE_C32)
        self.burst_preamble_correlator_0 = burst.preamble_correlator(4, 0.5, (pre_bits))
        self.burst_length_detect_c_0 = burst.length_detect_c()
        (self.burst_length_detect_c_0).set_min_output_buffer(20800)
        self.burst_correlator_filter_0 = burst.correlator_filter(100, 1e-4, -10)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.pyqt_const_plot_0, 'cpdus'))
        self.msg_connect((self.burst_length_detect_c_0, 'cpdus'), (self.pyqt_cpower_plot_0_0, 'cpdus'))
        self.msg_connect((self.es_handler_pdu_0, 'pdus_out'), (self.burst_length_detect_c_0, 'cpdus'))
        self.msg_connect((self.es_trigger_edge_f_0, 'edge_event'), (self.es_handler_pdu_0, 'handle_event'))
        self.msg_connect((self.es_trigger_edge_f_0, 'which_stream'), (self.es_sink_0, 'schedule_event'))
        self.connect((self.burst_correlator_filter_0, 0), (self.es_trigger_edge_f_0, 0))
        self.connect((self.burst_correlator_filter_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.burst_preamble_correlator_0, 0), (self.burst_correlator_filter_0, 0))
        self.connect((self.es_trigger_edge_f_0, 0), (self.es_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.burst_preamble_correlator_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.es_trigger_edge_f_0, 1))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_time_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "psk_burst_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_pre_bits(self):
        return self.pre_bits

    def set_pre_bits(self, pre_bits):
        self.pre_bits = pre_bits

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.set_samps_per_symb(int(self.samp_rate/self.baud))
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samps_per_symb(int(self.samp_rate/self.baud))

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

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

    def get_rrc_filter_taps(self):
        return self.rrc_filter_taps

    def set_rrc_filter_taps(self, rrc_filter_taps):
        self.rrc_filter_taps = rrc_filter_taps


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser


def main(top_block_cls=psk_burst_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
