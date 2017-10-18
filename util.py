
# Standard IPv4 Internet checksum
# https://tools.ietf.org/html/rfc1071
def ipv4_checksum(data):
    # If the length is not a multiple of 2, start with the odd end byte
    pos = len(data)
    if (pos & 1):
        pos -= 1
        sum = ord(data[pos])
    else:
        sum = 0

    # Sum everything as 16-bit words
    while pos > 0:
        pos -= 2
        sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

    # We only want 16 bits
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    # One's complement
    result = (~ sum) & 0xffff

    # Keep lower 16 bits and swap bytes
    result = result >> 8 | ((result & 0xff) << 8)
    return chr(result / 256) + chr(result % 256)
