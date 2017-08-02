#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fsk Rx 1
# Generated: Thu Jun 15 08:39:03 2017
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
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import kiss
import sys
import time
from gnuradio import qtgui


class fsk_rx_1(gr.top_block, Qt.QWidget):

    def __init__(self, addr='0.0.0.0', port='52001', rx_gain=38):
        gr.top_block.__init__(self, "Fsk Rx 1")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Fsk Rx 1")
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

        self.settings = Qt.QSettings("GNU Radio", "fsk_rx_1")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.addr = addr
        self.port = port
        self.rx_gain = rx_gain

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 500000
        self.baud = baud = 10e3
        self.samps_per_symb = samps_per_symb = int(samp_rate/baud)
        self.mult = mult = (samp_rate)/2/3.141593
        self.freq = freq = 433e6
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_subdev_spec('A:B', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(freq, samp_rate/2), 0)
        self.uhd_usrp_source_0_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.kiss_pdu_to_kiss_0 = kiss.pdu_to_kiss()
        self.kiss_hdlc_deframer_0 = kiss.hdlc_deframer(check_fcs=True, max_length=10000)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=samps_per_symb,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0, 16)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", addr, port, 1024, True)
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.kiss_pdu_to_kiss_0, 'in'))
        self.msg_connect((self.kiss_pdu_to_kiss_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.connect((self.digital_descrambler_bb_0, 0), (self.kiss_hdlc_deframer_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.digital_descrambler_bb_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.digital_gmsk_demod_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fsk_rx_1")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0_0.set_gain(self.rx_gain, 0)


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samps_per_symb(int(self.samp_rate/self.baud))
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(self.freq, self.samp_rate/2), 0)
        self.set_mult((self.samp_rate)/2/3.141593)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_samps_per_symb(int(self.samp_rate/self.baud))

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

    def get_mult(self):
        return self.mult

    def set_mult(self, mult):
        self.mult = mult

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(self.freq, self.samp_rate/2), 0)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--addr", dest="addr", type="string", default='0.0.0.0',
        help="Set addr [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default='52001',
        help="Set port [default=%default]")
    parser.add_option(
        "", "--rx-gain", dest="rx_gain", type="intx", default=38,
        help="Set rx_gain [default=%default]")
    return parser


def main(top_block_cls=fsk_rx_1, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(addr=options.addr, port=options.port, rx_gain=options.rx_gain)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
