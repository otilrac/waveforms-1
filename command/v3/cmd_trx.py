#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Cmd Trx
# Generated: Thu Jun 15 12:47:31 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('/home/root/.grc_gnuradio')))

from fsk_rx_hier import fsk_rx_hier  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from tx_ao40_dbpsk_hier import tx_ao40_dbpsk_hier  # grc-generated hier_block
import time


class cmd_trx(gr.top_block):

    def __init__(self, addr='0.0.0.0', alpha=0.5, bb_gain=.4, fsk_dev=10000, lpf_cutoff=15e3, lpf_trans=1e3, port='52001', rx_baud=10000, rx_correct=0, rx_freq=1265e6, rx_gain=20, samps_per_symb=2, tx_correct=0, tx_freq=2395e6, tx_gain=75, tx_offset=0):
        gr.top_block.__init__(self, "Cmd Trx")

        ##################################################
        # Parameters
        ##################################################
        self.addr = addr
        self.alpha = alpha
        self.bb_gain = bb_gain
        self.fsk_dev = fsk_dev
        self.lpf_cutoff = lpf_cutoff
        self.lpf_trans = lpf_trans
        self.port = port
        self.rx_baud = rx_baud
        self.rx_correct = rx_correct
        self.rx_freq = rx_freq
        self.rx_gain = rx_gain
        self.samps_per_symb = samps_per_symb
        self.tx_correct = tx_correct
        self.tx_freq = tx_freq
        self.tx_gain = tx_gain
        self.tx_offset = tx_offset

        ##################################################
        # Variables
        ##################################################
        self.tx_samp_rate = tx_samp_rate = 250000
        self.rx_samp_rate = rx_samp_rate = 100000

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
        self.uhd_usrp_source_0_0.set_samp_rate(rx_samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(rx_freq+rx_correct, rx_samp_rate/2), 0)
        self.uhd_usrp_source_0_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(tx_samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(tx_freq+tx_correct, tx_offset), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.tx_ao40_dbpsk_hier_0 = tx_ao40_dbpsk_hier(
            alpha=0.5,
            bb_gain=.5,
            samp_rate=tx_samp_rate,
            samps_per_symb=samps_per_symb,
        )
        self.fsk_rx_hier_0 = fsk_rx_hier(
            baud=rx_baud,
            samp_rate=rx_samp_rate,
            lpf_cutoff=lpf_cutoff,
            lpf_trans=lpf_trans,
            fsk_dev=fsk_dev,
        )
        self.blocks_socket_pdu_1 = blocks.socket_pdu("TCP_SERVER", addr, '52001', 10000, False)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_1, 'pdus'), (self.tx_ao40_dbpsk_hier_0, 'in'))
        self.msg_connect((self.fsk_rx_hier_0, 'out'), (self.blocks_socket_pdu_1, 'pdus'))
        self.connect((self.tx_ao40_dbpsk_hier_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.fsk_rx_hier_0, 0))

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

    def get_fsk_dev(self):
        return self.fsk_dev

    def set_fsk_dev(self, fsk_dev):
        self.fsk_dev = fsk_dev
        self.fsk_rx_hier_0.set_fsk_dev(self.fsk_dev)

    def get_lpf_cutoff(self):
        return self.lpf_cutoff

    def set_lpf_cutoff(self, lpf_cutoff):
        self.lpf_cutoff = lpf_cutoff
        self.fsk_rx_hier_0.set_lpf_cutoff(self.lpf_cutoff)

    def get_lpf_trans(self):
        return self.lpf_trans

    def set_lpf_trans(self, lpf_trans):
        self.lpf_trans = lpf_trans
        self.fsk_rx_hier_0.set_lpf_trans(self.lpf_trans)

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_rx_baud(self):
        return self.rx_baud

    def set_rx_baud(self, rx_baud):
        self.rx_baud = rx_baud
        self.fsk_rx_hier_0.set_baud(self.rx_baud)

    def get_rx_correct(self):
        return self.rx_correct

    def set_rx_correct(self, rx_correct):
        self.rx_correct = rx_correct
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(self.rx_freq+self.rx_correct, self.rx_samp_rate/2), 0)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(self.rx_freq+self.rx_correct, self.rx_samp_rate/2), 0)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0_0.set_gain(self.rx_gain, 0)


    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb
        self.tx_ao40_dbpsk_hier_0.set_samps_per_symb(self.samps_per_symb)

    def get_tx_correct(self):
        return self.tx_correct

    def set_tx_correct(self, tx_correct):
        self.tx_correct = tx_correct
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)


    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.tx_freq+self.tx_correct, self.tx_offset), 0)

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.tx_samp_rate)
        self.tx_ao40_dbpsk_hier_0.set_samp_rate(self.tx_samp_rate)

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.uhd_usrp_source_0_0.set_samp_rate(self.rx_samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(uhd.tune_request(self.rx_freq+self.rx_correct, self.rx_samp_rate/2), 0)
        self.fsk_rx_hier_0.set_samp_rate(self.rx_samp_rate)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--addr", dest="addr", type="string", default='0.0.0.0',
        help="Set addr [default=%default]")
    parser.add_option(
        "", "--alpha", dest="alpha", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set alpha [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(.4),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--fsk-dev", dest="fsk_dev", type="eng_float", default=eng_notation.num_to_str(10000),
        help="Set FSK Deviation [default=%default]")
    parser.add_option(
        "", "--lpf-cutoff", dest="lpf_cutoff", type="eng_float", default=eng_notation.num_to_str(15e3),
        help="Set LPF Cutoff [default=%default]")
    parser.add_option(
        "", "--lpf-trans", dest="lpf_trans", type="eng_float", default=eng_notation.num_to_str(1e3),
        help="Set LPF Trans Width [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default='52001',
        help="Set port [default=%default]")
    parser.add_option(
        "", "--rx-baud", dest="rx_baud", type="eng_float", default=eng_notation.num_to_str(10000),
        help="Set RX Baud Rate [default=%default]")
    parser.add_option(
        "", "--rx-correct", dest="rx_correct", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set rx_correct [default=%default]")
    parser.add_option(
        "", "--rx-freq", dest="rx_freq", type="eng_float", default=eng_notation.num_to_str(1265e6),
        help="Set RX Freq [default=%default]")
    parser.add_option(
        "", "--rx-gain", dest="rx_gain", type="intx", default=20,
        help="Set RX Gain [default=%default]")
    parser.add_option(
        "", "--samps-per-symb", dest="samps_per_symb", type="eng_float", default=eng_notation.num_to_str(2),
        help="Set samps_per_symb [default=%default]")
    parser.add_option(
        "", "--tx-correct", dest="tx_correct", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_correct [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(2395e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(75),
        help="Set tx_gain [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_offset [default=%default]")
    return parser


def main(top_block_cls=cmd_trx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, fsk_dev=options.fsk_dev, lpf_cutoff=options.lpf_cutoff, lpf_trans=options.lpf_trans, port=options.port, rx_baud=options.rx_baud, rx_correct=options.rx_correct, rx_freq=options.rx_freq, rx_gain=options.rx_gain, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, tx_offset=options.tx_offset)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
