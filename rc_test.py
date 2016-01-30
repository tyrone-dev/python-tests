#!/usr/bin/env python

# debug script for debugging rc.local issues on rasperry pi

# docstring

__author__ = "Tyrone van Balla"
__version__ = "Version 0.x.1"
__description__ = "Debugs rc.local startup events"

import argparse
import threading
import logging
import time

# argument parser

parser = argparse.ArgumentParser(description="Tests rc.local functioning on raspberry pi")

#parser.add_argument("loops", help="Specify number of loops to run", type=int)
#parser.add_argument("-t", "--threads", help="Number of concurrent thread", type=int, default=1)
parser.add_argument("threads", help="Number of concurrent thread", type=int)
parser.add_argument("-v", "--verbosity", help="Change verbosity of logger", action="count", default=0)
#parser.add_argument("-n", "--nettest", help="Run network test", action="store_true")
parser.add_argument("-n", "--nettest", help="Run network test;specify number of threads", type=int)

args = parser.parse_args()

threads = []

# logger 
logger = logging.getLogger(__name__)

if args.verbosity == 0:
    level = logging.INFO
else:
    level = logging.DEBUG

logger.setLevel(level)

# file handler
fh = logging.FileHandler("rc.local.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName)s  - %(levelname)s -%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# functions
def worker(thread_number):
	logger.debug('Starting...')
	print 'Worked: %i' %thread_number
	time.sleep(2)
	logger.debug('Exiting...')
	return

def threader(numThreads):

	print "Number of threads is: {}".format(numThreads)
	for i in range (1, numThreads+1):
		name = "thread %s" %i
		t = threading.Thread(name=name, target=worker, args=(i,))
		threads.append(t)
		t.start() # thread starts running the moment this is executed
		#t.join() # this? 

def network_test(number_packets, mode, threads):
    logger.info("Network Packet Test: Mode:  %s\n Sending %i pkts for %i thread/s" %(mode, number_packets, threads))
    '''
    simple packet tx/rx test on startup of device
    
    modes: deliberate - sends packet and waits for ACK (rx pkt)
           listen - listens for packets and sends ACK (tx pkt)
    
    number of packets: number of pkts to send

    thread: number of pkt sending threads (# pkts is per thread)
    '''
    import socket

    if mode == 'deliberate':
        broadcast_tuple = ('<broadcast>', 10000)
        d_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        d_socket.bind(('', 10000))
        d_socket.setsockopt(socket.SOL_SOCKET, SO_BROADCAST, 1)
        
        deliberate_search(d_socket, mesg, broadcast_tuple, stop_event)
        pass
    elif mode == 'listen':
        pass
    else:
        logger.error("Unrecognized network test mode specified")
        return
             
def deliberate_search(d_socket, message, broadcast_tuple, stop_event):
    """
    Send probe packets to look for slave.
    Separate thread is used to send these packets continuously
    """
    
    # thread stops when all nodes are connected or on timeout
    while (not stop_event.isSet()):
        sent = master_socket.sendto(message, broadcast_tuple)

    logger.debug("Exiting ping packet thread . . .")

# main
logger.info("\nTest session started . . .")
threader(args.threads)

if args.nettest:
    import socket
    network_test(10, "deliberate", args.nettest)

# end
#logger.info("Test session complete\n\n")
