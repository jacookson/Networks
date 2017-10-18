#
# send3.py
#
# rdt3.0 ('Alternating Bit') protocol sender
# Uses UDP as the 'Unreliable transport'
#
# See section 3.4.1 in Computer Networking: A Top-Down Approach,
#   by Kurose and Ross, 7th edition
#

# Get some socket functions and constants
from socket import socket, AF_INET, SOCK_DGRAM, timeout

# 16-bit (2 bytes) Internet checksum
from util import ipv4_checksum

###########################################################
### Receiver host and port. Set these as appropriate ###
###########################################################
dest = ('10.0.0.2', 12000)

# Create a UDP socket. We use UDP as our unreliable transport.
sock = socket(AF_INET, SOCK_DGRAM)

# Use a 1 second retransmission timeout. recvfrom() will block for 1 second.
# and then raise a timeout exception if no packet has arrived
sock.settimeout(1)

# Initial sequence number
seqnum = 0

# Send some data to the receiver
for data in 'ABCDEFGHIJ':

    # Data packet format is cksum + seqnum + data
    # (2 bytes) + (1 byte) + (data bytes)
    cksum = ipv4_checksum(data)
    packet = cksum + str(seqnum) + data

    ack_received = False
    retransmit = 0
    while not ack_received:

        # Send data (at least once)
        sock.sendto(packet, dest)
        if retransmit == 0:
            print "Sending packet to %s: seqnum = %d, cksum = %s" % (repr(dest), seqnum, repr(cksum))
        else:
            print "Retransmit packet: seqnum = %d, cksum = %s" % (seqnum, repr(cksum))

        # Try to read ACK from receiver. recvfrom() will timeout
        # 'Wait for ACK0' or 'Wait for ACK1' state
        try:
            ackpacket, address = sock.recvfrom(2048)
        except timeout:
            # On timeout, do nothing, just loop back and retransmit
            print "Timeout! Did not receive ACK%s" % str(seqnum)
        else:
            # Potential ACK received, extract checksum and seq number
            # ACK packet format is checksum + 'ACK' + seqnum
            # (2 bytes) + (3 bytes) + (1 byte)
            checksum = ackpacket[:2]  # 1st two bytes are checksum
            ack_seq = ackpacket[5]    # 6th byte is ACK seqnum
            print "Received ACK%s from %s" % (ack_seq, repr(address))

            # If ACK is valid, this will stop the inner loop
            # so we can send another packet
            if ipv4_checksum(ackpacket[2:]) == checksum and ack_seq == str(seqnum):
                ack_received = True

        # Otherwise, loop back and retransmit (timeout or bad ACK)
        retransmit += 1

    # Flip sequence number and loop back to get more data (outer loop)
    seqnum = 1 - seqnum
