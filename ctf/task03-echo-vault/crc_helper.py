"""ECHO Vault checksum primitives (participant). Documented so you need not guess a variant.

A checksum is error detection, not authentication.
"""
import binascii


def crc16(data):
    """CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF, no reflection, xorout 0. The frame checksum."""
    return binascii.crc_hqx(data, 0xFFFF)


def crc32(data):
    """Standard CRC-32 (reflected, poly 0xEDB88320), as used by binascii.crc32."""
    return binascii.crc32(data) & 0xFFFFFFFF
