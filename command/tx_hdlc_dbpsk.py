#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Hdlc Dbpsk
# Generated: Tue May 23 01:42:54 2017
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import kiss
import time


class tx_hdlc_dbpsk(gr.top_block):

    def __init__(self, addr='127.0.0.1', alpha=0.5, bb_gain=.5, port='4000', post_bytes=7, pre_bytes=100, samp_rate=500e3, samps_per_symb=4, tx_correct=0, tx_freq=2395e6, tx_gain=40, tx_offset=250e3):
        gr.top_block.__init__(self, "Tx Hdlc Dbpsk")

        ##################################################
        # Parameters
        ##################################################
        self.addr = addr
        self.alpha = alpha
        self.bb_gain = bb_gain
        self.port = port
        self.post_bytes = post_bytes
        self.pre_bytes = pre_bytes
        self.samp_rate = samp_rate
        self.samps_per_symb = samps_per_symb
        self.tx_correct = tx_correct
        self.tx_freq = tx_freq
        self.tx_gain = tx_gain
        self.tx_offset = tx_offset

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(tx_freq+tx_correct, tx_offset), 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.kiss_nrzi_encode_0 = kiss.nrzi_encode()
        self.kiss_hdlc_framer_0 = kiss.hdlc_framer(preamble_bytes=pre_bytes, postamble_bytes=post_bytes)
        self.digital_dxpsk_mod_0 = digital.dbpsk_mod(
        	samples_per_symbol=samps_per_symb,
        	excess_bw=alpha,
        	mod_code="gray",
        	verbose=False,
        	log=False)

        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_SERVER", addr, port, 255, False)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'pl2')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((bb_gain, ))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.kiss_hdlc_framer_0, 'in'))
        self.msg_connect((self.kiss_hdlc_framer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.kiss_nrzi_encode_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_dxpsk_mod_0, 0))
        self.connect((self.digital_dxpsk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.kiss_nrzi_encode_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))

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

    def get_post_bytes(self):
        return self.post_bytes

    def set_post_bytes(self, post_bytes):
        self.post_bytes = post_bytes

    def get_pre_bytes(self):
        return self.pre_bytes

    def set_pre_bytes(self, pre_bytes):
        self.pre_bytes = pre_bytes

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


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--addr", dest="addr", type="string", default='127.0.0.1',
        help="Set addr [default=%default]")
    parser.add_option(
        "", "--alpha", dest="alpha", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set alpha [default=%default]")
    parser.add_option(
        "", "--bb-gain", dest="bb_gain", type="eng_float", default=eng_notation.num_to_str(.5),
        help="Set bb_gain [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="string", default='4000',
        help="Set port [default=%default]")
    parser.add_option(
        "", "--post-bytes", dest="post_bytes", type="intx", default=7,
        help="Set post_bytes [default=%default]")
    parser.add_option(
        "", "--pre-bytes", dest="pre_bytes", type="intx", default=100,
        help="Set pre_bytes [default=%default]")
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
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(40),
        help="Set tx_gain [default=%default]")
    parser.add_option(
        "", "--tx-offset", dest="tx_offset", type="eng_float", default=eng_notation.num_to_str(250e3),
        help="Set tx_offset [default=%default]")
    return parser


def main(top_block_cls=tx_hdlc_dbpsk, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(addr=options.addr, alpha=options.alpha, bb_gain=options.bb_gain, port=options.port, post_bytes=options.post_bytes, pre_bytes=options.pre_bytes, samp_rate=options.samp_rate, samps_per_symb=options.samps_per_symb, tx_correct=options.tx_correct, tx_freq=options.tx_freq, tx_gain=options.tx_gain, tx_offset=options.tx_offset)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
