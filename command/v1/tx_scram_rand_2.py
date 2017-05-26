#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Scram Rand 2
# Generated: Sun May 21 03:05:30 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import pmt
import time
import vtgs


class tx_scram_rand_2(gr.top_block):

    def __init__(self, addr='127.0.0.1', alpha=0.5, bb_gain=1, port='4000', samp_rate=500e3, samps_per_symb=4, tx_correct=0, tx_freq=2395e6, tx_gain=20, tx_offset=0, tx_period=500, update_period=2000):
        gr.top_block.__init__(self, "Tx Scram Rand 2")

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
        self.tx_period = tx_period
        self.update_period = update_period

        ##################################################
        # Blocks
        ##################################################
        self.vtgs_ao40_encoder_0 = vtgs.ao40_encoder(False, 449838109)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_time_source('gpsdo', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(tx_freq+tx_correct, tx_offset), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.digital_map_bb_0 = digital.map_bb((1,0))
        self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
        	samples_per_symbol=samps_per_symb,
        	excess_bw=alpha,
        	mod_code="gray",
        	verbose=False,
        	log=False)

        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (768,5232))
        self.blocks_random_pdu_0 = blocks.random_pdu(256, 256, chr(0xFF), 2)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((bb_gain, ))
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.intern("TEST"), tx_period)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), update_period)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 1, 768)), True)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_message_strobe_0_0, 'strobe'), (self.vtgs_ao40_encoder_0, 'in'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.blocks_message_strobe_0_0, 'set_msg'))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_dxpsk_mod_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_dxpsk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.vtgs_ao40_encoder_0, 0), (self.blocks_stream_mux_0, 1))

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
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_samps_per_symb(self):
        return self.samps_per_symb

    def set_samps_per_symb(self, samps_per_symb):
        self.samps_per_symb = samps_per_symb

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

    def get_tx_period(self):
        return self.tx_period

    def set_tx_period(self, tx_period):
        self.tx_period = tx_period
        self.blocks_message_strobe_0_0.set_period(self.tx_period)

    def get_update_period(self):
        return self.update_period

    def set_update_period(self, update_period):
        self.update_period = update_period
        self.blocks_message_strobe_0.set_period(self.update_period)


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
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(500e3),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "", "--samps-per-symb", dest="samps_per_symb", type="eng_float", default=eng_notation.num_to_str(4),
        help="Set samps_per_symb [default=%default]")
    parser.add_option(
        "", "--tx-correct", dest="tx_correct", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_correct [default=%default]")
    parser.add_option(
        "", "--tx-freq", dest="tx_freq", type="eng_float", default=eng_notation.num_to_str(2395e6),
        help="Set tx_freq [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set tx_gain [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set tx_offset [default=%default]")
    parser.add_option(
        "", "--tx-period", dest="tx_period", type="eng_float", default=eng_notation.num_to_str(500),
        help="Set tx_period [default=%default]")
    parser.add_option(
        "", "--update-period", dest="update_period", type="eng_float", default=eng_notation.num_to_str(2000),
        help="Set update_period [default=%default]")
    return parser


def main(top_block_cls=tx_scram_rand_2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, port=options.port, samp_rate=options.samp_rate, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, tx_offset=options.tx_offset, tx_period=options.tx_period, update_period=options.update_period)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
