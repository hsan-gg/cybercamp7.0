"""Recover the lamp's rules, then prove them. Fill the four TODOs.
Run: python workshop.py --host 127.0.0.1 --port 9003"""

import argparse
import binascii
import socket
import struct

from wire import ProtocolError, encode, receive

HELLO, PING = 0x01, 0x02

# TODO 1 — the two command codes.
SET_BRIGHTNESS = 0x20
READ_STATUS = 0x22


def encode_level(level):
    # TODO 2 — turn a 0-100 value into one byte.
    return ((level ^ 0x5A) + 7) & 0xFF


def compute_check(nonce, sequence, encoded):
    # TODO 3 — build the 4-byte check (binascii.crc32 over a small buffer).
    buf = struct.pack("<IHB", nonce, sequence, encoded)
    return binascii.crc32(buf) & 0xFFFFFFFF


def decode_status(payload):
    # TODO 4 — return (brightness, temperature_celsius).
    brightness, temperature = struct.pack("<BH", payload)
    return brightness, temperature / 100


# ---- supplied plumbing; you should not need to change the rest ----
class Lamp:
    def __init__(self, host, port):
        self.sequence = 0
        self.sock = socket.create_connection((host, port), timeout=5)
        reply = self._request(HELLO)
        self.name, self.nonce = reply[:-4], int.from_bytes(reply[-4:], "little")
        print(
            "Connected to %s (nonce %08x)"
            % (self.name.decode("ascii", "replace"), self.nonce)
        )

    def close(self):
        self.sock.close()

    def _request(self, opcode, payload=b""):
        self.sequence = (self.sequence + 1) & 0xFFFF
        self.sock.sendall(encode(opcode, self.sequence, payload))
        reply = receive(self.sock)
        if reply.sequence != self.sequence:
            raise ProtocolError("Reply identifier mismatch")
        if reply.opcode == 0xFF:
            raise ProtocolError(
                "Server error: " + reply.payload.decode("utf-8", "replace")
            )
        if reply.opcode != (opcode | 0x80):
            raise ProtocolError("Unexpected reply type %02x" % reply.opcode)
        return reply.payload

    def set_brightness(self, level):
        encoded = encode_level(level)
        check = compute_check(self.nonce, (self.sequence + 1) & 0xFFFF, encoded)
        if self._request(
            SET_BRIGHTNESS, bytes([encoded]) + struct.pack("<I", check)
        ) != bytes([encoded]):
            raise ProtocolError("SET_BRIGHTNESS did not echo the encoded byte")

    def read_status(self):
        return decode_status(self._request(READ_STATUS))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9003)
    parser.add_argument("--brightness", type=int, default=60)
    args = parser.parse_args()
    if SET_BRIGHTNESS is None or READ_STATUS is None:
        raise SystemExit("Fill TODO 1 first.")

    lamp = Lamp(args.host, args.port)
    try:
        lamp.set_brightness(args.brightness)
        brightness, temperature = lamp.read_status()
        print("STATUS brightness=%d temperature=%.2f C" % (brightness, temperature))
        print("Confirmed." if brightness == args.brightness else "Mismatch.")
    finally:
        lamp.close()


if __name__ == "__main__":
    main()
