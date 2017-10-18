#
# recv3.py
#
# rdt3.0 ('Alternating Bit') protocol receiver
# Uses UDP as the 'Unreliable transport'
#
# See section 3.4.1 in Computer Networking: A Top-Down Approach,
#   by Kurose and Ross, 7th edition
#

# Get some socket functions and constants
from socket import socket, AF_INET, SOCK_DGRAM

# 16-bit (2 bytes) Internet checksum
from util import ipv4_checksum

# Make an ACK packet. 
# ACK packet format is checksum + 'ACK' + seqnum
# (2 bytes) + (3 bytes) + (1 byte)
def make_ack(seqnum):
    data = "ACK" + str(seqnum)
    cksum = ipv4_checksum(data)
    return cksum + data

# Deliver data to the application layer
def deliver_data(data):
    print "Data delivered to app layer: " + data


# Create a UDP socket and listen
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', 12000))  # '' for address means listen on all local addresses
print "Listening on " + repr(sock.getsockname())

# First packet received should have sequence num 0
expected_seqnum = 0

# Loop forever, waiting for packets to arrive.
# With normal operation, we're simply alternating between
# the "wait for 0 from below" and "Wait for 1 from below" states
# by flipping the expected sequence number between 0 and 1
while True:
    # Receive a packet
    packet, address = sock.recvfrom(2048)

    # Extract header fields and data (as strings)
    # Data packet format is cksum + seqnum + data
    # (2 bytes) + (1 byte) + (data bytes)
    cksum = packet[:2]   # 1st two bytes are checksum
    seqnum = packet[2]   # 3rd byte is seqnum
    data = packet[3:]    # the rest is data
    print "Received packet from %s: seqnum=%s cksum=%s" % (address, seqnum, repr(cksum))

    # If checksum is OK and seqnum is what we expect, then
    # deliver data to app layer and send ACK.
    if ipv4_checksum(data) == cksum and seqnum == str(expected_seqnum):
        deliver_data(data)
        packet = make_ack(seqnum)
        sock.sendto(packet, address)
        print "Sent ACK%s" % seqnum

        # Flip expected seqnum for next packet, moving us to the other state.
        expected_seqnum = 1 - expected_seqnum
    else:
        # Otherwise, send ACK for last good packet received.
        # This will be the "other" sequence number.
        # This means we stay in the same state, still waiting for
        # the packet with the seqnum we expect
        packet = make_ack(1 - expected_seqnum)
        sock.sendto(packet, address)
        print "Sent ACK%s" % str(1 - expected_seqnum)
