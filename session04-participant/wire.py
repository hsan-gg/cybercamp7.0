"""Lamp protocol framing: envelope + CRC16. Supplied helper; do not edit."""
import binascii
import struct
from dataclasses import dataclass

MAGIC, VERSION, MAX_PAYLOAD = b"\xca\xfe", 1, 256
HEADER, CRC = struct.Struct("<2sBBHH"), struct.Struct("<H")


class ProtocolError(ValueError):
    pass


@dataclass(frozen=True)
class Frame:
    opcode: int
    sequence: int
    payload: bytes


def crc16(data):
    return binascii.crc_hqx(data, 0xFFFF)


def encode(opcode, sequence, payload=b""):
    if len(payload) > MAX_PAYLOAD:
        raise ProtocolError("Payload exceeds 256 bytes")
    header = HEADER.pack(MAGIC, VERSION, opcode, sequence, len(payload))
    return header + payload + CRC.pack(crc16(header[2:] + payload))


def read_exact(sock, length):
    data = bytearray()
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise EOFError("Connection closed before a complete message")
        data.extend(chunk)
    return bytes(data)


def receive(sock, trace=None):
    header = read_exact(sock, HEADER.size)
    magic, version, opcode, sequence, length = HEADER.unpack(header)
    if magic != MAGIC or version != VERSION:
        raise ProtocolError("Invalid magic or unsupported version")
    if length > MAX_PAYLOAD:
        raise ProtocolError("Payload exceeds 256 bytes")
    payload = read_exact(sock, length)
    crc_bytes = read_exact(sock, CRC.size)
    if trace:
        trace("RX", header + payload + crc_bytes)
    if CRC.unpack(crc_bytes)[0] != crc16(header[2:] + payload):
        raise ProtocolError("CRC mismatch")
    return Frame(opcode, sequence, payload)
