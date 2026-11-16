"""Supplied checksum helper. This describes CRC parameters, not frame layout."""

import binascii


def crc16(data):
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, refin/out false, xorout 0.

    Standard check: crc16(b'123456789') == 0x29B1.
    Infer which bytes are covered and how the result is stored from the traffic.
    This is a public checksum, not a key or authentication mechanism.
    """
    return binascii.crc_hqx(data, 0xFFFF)

