#!/usr/bin/env python
##################################################
# Title: E310 Serial to Ethernet Test
# Author: Zachary James Leffke
# Description: 
#   Test pyserial module on E310
# Generated: April 5, 2016
##################################################

import os
import sys
import time
import string
import serial
import socket
import threading
import random


from optparse import OptionParser
from datetime import datetime as date
    
if __name__ == '__main__':
    #ts = (date.datetime.utcnow()).strftime("%Y%m%d")

    #--------START Command Line option parser------------------------------------------------------
    usage = "usage: %prog <options>"
    parser = OptionParser(usage = usage)

    #----Serial/socket options----
    a_help = "Destination IP Address, [default=%default]"
    p_help = "Destination Port, [default=%default]"
    r_help = "Socket Write Speed [sec], [default=%default]"
    f_help = "source data file, [default=%default]"
    rand_help = "Enable random sleep, [default=%default]"

    parser.add_option("-a","--addr"  ,dest="addr"  ,action="store",type="string",default="127.0.0.1",help=a_help)
    parser.add_option("-p","--port"  ,dest="port"  ,action="store",type="int",default="4000",help=p_help)
    parser.add_option("-r","--rate"  ,dest="rate"  ,action="store",type="float" ,default="0.044",help=r_help)
    parser.add_option("-f","--file"  ,dest="file"  ,action="store",type="string",default="zeros.dat",help=f_help)
    parser.add_option("","--rand"  ,dest="rand"  ,action="store",type="int",default="0",help=rand_help)

    (options, args) = parser.parse_args()
    #--------END Command Line option parser------------------------------------------------------

    print options.file
    f = open(options.file, 'r') 
    data = f.read()
    print len(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (options.addr, options.port))
    while 1:
        sock.sendto(data, (options.addr, options.port))
        if options.rand != 0:
            sleep_time = random.uniform(0, 2)
            print 'Sleeping for:', str(sleep_time)
            time.sleep(sleep_time)
        else:
            time.sleep(options.rate)
    
    sys.exit()
