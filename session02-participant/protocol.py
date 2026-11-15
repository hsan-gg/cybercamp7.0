"""Session 2 reference codec/client. Python standard library only."""
import binascii
import socket
import struct
from dataclasses import dataclass

MAGIC, VERSION, MAX_PAYLOAD = b"\xca\xfe", 1, 256
HEADER, CRC, STATUS_DATA = struct.Struct("<2sBBHH"), struct.Struct("<H"), struct.Struct("<Bh")
HELLO, PING, STATUS, SET_LED, ERROR = 1, 2, 3, 4, 0xFF


class ProtocolError(ValueError):
    pass


class ServerError(ProtocolError):
    """A valid error response; framing and the TCP connection remain usable."""


@dataclass(frozen=True)
class Frame:
    opcode: int
    sequence: int
    payload: bytes


def encode(opcode, sequence, payload=b""):
    if len(payload) > MAX_PAYLOAD:
        raise ProtocolError("Payload exceeds 256 bytes")
    header = HEADER.pack(MAGIC, VERSION, opcode, sequence, len(payload))
    crc = binascii.crc_hqx(header[2:] + payload, 0xFFFF)
    return header + payload + CRC.pack(crc)


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
    if CRC.unpack(crc_bytes)[0] != binascii.crc_hqx(header[2:] + payload, 0xFFFF):
        raise ProtocolError("CRC mismatch")
    return Frame(opcode, sequence, payload)


class Client:
    def __init__(self, host, port, trace=None):
        self.trace, self.sequence = trace, 0
        self.sock = socket.create_connection((host, port), timeout=5)
        try:
            self.name = self.request(HELLO).decode("ascii")
        except Exception:
            self.close()
            raise

    def close(self):
        self.sock.close()

    def request(self, opcode, payload=b""):
        self.sequence = (self.sequence + 1) & 0xFFFF
        wire = encode(opcode, self.sequence, payload)
        if self.trace:
            self.trace("TX", wire)
        self.sock.sendall(wire)
        reply = receive(self.sock, self.trace)
        if reply.sequence != self.sequence:
            raise ProtocolError("Response request identifier mismatch")
        if reply.opcode == ERROR:
            raise ServerError(reply.payload.decode("utf-8", errors="replace"))
        if reply.opcode != (opcode | 0x80):
            raise ProtocolError("Unexpected response command")
        return reply.payload

    def perform(self, action):
        if action == "ping":
            reply = self.request(PING)
            if reply != b"PONG":
                raise ProtocolError("Invalid PING response")
            return "PONG"
        if action == "status":
            reply = self.request(STATUS)
            if len(reply) != STATUS_DATA.size:
                raise ProtocolError("STATUS response must contain three bytes")
            led, temperature = STATUS_DATA.unpack(reply)
            if led not in (0, 1):
                raise ProtocolError("Invalid LED state")
            return "LED: %s | Simulated temperature: %.2f C" % ("ON" if led else "OFF", temperature / 100)
        if action in ("on", "off"):
            payload = bytes([int(action == "on")])
            if self.request(SET_LED, payload) != payload:
                raise ProtocolError("SET_LED acknowledgment mismatch")
            return "LED set to " + action.upper()
        raise ValueError("Unknown action: " + action)
