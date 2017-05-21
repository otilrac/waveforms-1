#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Trx Scram Sock
# Generated: Sun May 21 01:27:12 2017
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
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import sip
import sys
import vtgs
from gnuradio import qtgui


class trx_scram_sock(gr.top_block, Qt.QWidget):

    def __init__(self, addr='127.0.0.1', alpha=0.5, bb_gain=1, port='4000', samp_rate=250e3, samps_per_symb=2, tx_correct=0, tx_freq=2402e6, tx_gain=20, tx_offset=50e3):
        gr.top_block.__init__(self, "Trx Scram Sock")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Trx Scram Sock")
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

        self.settings = Qt.QSettings("GNU Radio", "trx_scram_sock")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.addr = addr
        self.alpha = alpha
        self.bb_gain = bb_gain
        self.port = port
        self.samp_rate = samp_rate
        self.samps_per_symb = samps_per_symb
        self.tx_correct = tx_correct
        self.tx_freq = tx_freq
        self.tx_gain = tx_gain
        self.tx_offset = tx_offset

        ##################################################
        # Blocks
        ##################################################
        self.vtgs_mult_scrambler_0 = vtgs.mult_scrambler(17, 0x3FFFF)
        self.vtgs_ao40_encoder_0 = vtgs.ao40_encoder(False, 449838109)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

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
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.digital_map_bb_0 = digital.map_bb((1,0))
        self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
        	samples_per_symbol=samps_per_symb,
        	excess_bw=alpha,
        	mod_code="gray",
        	verbose=False,
        	log=False)

        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (768,5232))
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_SERVER", addr, port, 10000, False)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((bb_gain, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 100e3, 1, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 1, 768)), True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.vtgs_ao40_encoder_0, 'in'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_dxpsk_mod_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_dxpsk_mod_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.vtgs_mult_scrambler_0, 0))
        self.connect((self.vtgs_ao40_encoder_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.vtgs_mult_scrambler_0, 0), (self.blocks_pack_k_bits_bb_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "trx_scram_sock")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.blocks_multiply_const_vxx_0.set_k((self.bb_gain, ))

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

    def get_tx_correct(self):
        return self.tx_correct

    def set_tx_correct(self, tx_correct):
        self.tx_correct = tx_correct

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--addr", dest="addr", type="string", default='127.0.0.1',
        help="Set addr [default=%default]")
    parser.add_option(
        "", "--alpha", dest="alpha", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set alpha [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default='4000',
        help="Set port [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(250e3),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--samps-per-symb", dest="samps_per_symb", type="eng_float", default=eng_notation.num_to_str(2),
        help="Set samps_per_symb [default=%default]")
    parser.add_option(
        "", "--tx-correct", dest="tx_correct", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_correct [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(2402e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set tx_gain [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(50e3),
        help="Set tx_offset [default=%default]")
    return parser


def main(top_block_cls=trx_scram_sock, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, port=options.port, samp_rate=options.samp_rate, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, tx_offset=options.tx_offset)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
