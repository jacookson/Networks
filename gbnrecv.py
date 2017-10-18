# Get some socket functions and constants
from socket import socket, AF_INET, SOCK_DGRAM

# 16-bit (2 bytes) Internet checksum
from util import ipv4_checksum

def make_ack(seqnum):
    data = "ACK" + str(seqnum)
    cksum = ipv4_checksum(data)
    return cksum + data

def deliver_data(data):
    print "Data delivered to app later: " + data

# Initial sequence number
exp_seqnum = 0

# Create a UDP socket and listen
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 12000))  # '' for address means listen on all local addresses
print "Listening on " + repr(sock.getsockname())

# Loop forever, waiting for packets to arrive.
# then deal with each as they arrive, checking
# their seqnum to ensure order and responding 
# with appropriate ACKs
while True:
    # Receive a packet
    packet, address = sock.recvfrom(2048)
    
    # Extract header fields and data (as strings)
    # Data packet format is cksum + seqnum + data
    # (2 bytes) + (1 byte) + (data bytes)                                 # will have to account for length or something
    cksum = packet[:2]   # 1st two bytes are checksum
    seqnum = packet[2]   # 3rd byte is seqnum
    data = packet[3:]    # the rest is data
    print "Received packet from %s: seqnum=%s cksum=%s" % (address, seqnum, repr(cksum))

    # If checksum is OK and seqnum is what we expect, then
    # deliver data to app layer and send ACK.
    if ipv4_checksum(data) == cksum and seqnum == str(exp_seqnum):
        deliver_data(data)
        packet = make_ack(seqnum)
        sock.sendto(packet, address)
        print "Sent ACK%s" % seqnum
        
        #increase by number of byites received
        #        expected_seqnum+=1
        
    else :
        # Otherwise, send ACK for last good packet received..
        # This means we stay in the same state, still waiting for
        # the packet with the seqnum we expect
        packet = make_ack(1 - exp_seqnum)
        sock.sendto(packet, address)
        
        #print "Sent ACK%s" % str(expected_seqnum- incremental value)
