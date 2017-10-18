# to allow for sending in parallel
import threading

# Get some socket functions and constants
from socket import socket, AF_INET, SOCK_DGRAM

# 16-bit (2 bytes) Internet checksum
from util import ipv4_checksum

dest = ('10.0.0.2', 12000)

# Create a UDP socket. We use UDP as our unreliable transport.
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(1)

# packet header:
# will be in the form
# 2 Byte cksum + 1 Byte seqnum + data of some number of bytes

# Initial (current) sequence number
seqnum = 1

# base of window
base = 1

# Window size
winsize = 5

#max seq num
max_seqnum = base + winsize # + 1

# Starting a thread so that the program is ready to receive
# ACKs at any time
class RecvThread(threading.Thread):
    def run(self):
        while True:
            ackpacket, address = sock.recvfrom(2048)
            
            # Potential ACK received, extract checksum and seq number
            # ACK packet format is checksum + 'ACK' + seqnum
            # (2 bytes) + (3 bytes) + (1 byte)
            checksum = ackpacket[:2]  # 1st two bytes are checksum
            ack_seq = ackpacket[5]    # 6th byte is ACK seqnum
            print "Received ACK%s from %s" % (ack_seq, repr(address))

            # If ACK is valid, this will move the base forward and thus the max seq num
            # so we can send additional packets
            if ipv4_checksum(ackpacket[2:]) == checksum and ack_seq > base:
                # this will adjust the window in accordance with a valid ACK
                max_seqnum = max_seqnum - base + ack_seq
                # move base forward
                base = ack_seq

RecvThread().start()

# message to send
message = 'ABCDEFGH'
while True:
    if seqnum < max_seqnum:
        data = message[seqnum]
        
        #data comes as cksum + seqnum + data
        # 2 byte, 1 byte, data
        cksum = ipv4_checksum(data)
        packet = cksum + str(seqnum) + data
        
        #send it
        sock.sendto(packet, dest)
        print "packets sent to %s: seqnum = %d, cksum = %s" % (repr(dest), seqnum, cksum)
        seqnum = seqnum + 1

