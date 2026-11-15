"""Provided plumbing: keep the live exercise focused on building messages."""
import argparse
import struct
from protocol import ERROR, receive


def receive_message(sock, trace=print):
    show = (lambda direction, wire: trace(direction + " " + wire.hex(" "))) if trace else None
    frame = receive(sock, show)
    return frame.opcode, frame.sequence, frame.payload


def receive_reply(sock, command, sequence, trace=print):
    reply_command, reply_sequence, payload = receive_message(sock, trace)
    if reply_sequence != sequence:
        raise ValueError("Response request identifier mismatch")
    if reply_command == ERROR:
        raise ValueError("Server error: " + payload.decode("utf-8", errors="replace"))
    if reply_command != (command | 0x80):
        raise ValueError("Unexpected response command")
    return payload


def decode_status(payload):
    if len(payload) != 3:
        raise ValueError("STATUS must contain three bytes")
    led, temperature = struct.unpack("<Bh", payload)
    if led not in (0, 1):
        raise ValueError("Invalid LED state")
    return led, temperature / 100


def parse_target(host, port):
    parser = argparse.ArgumentParser(description="Session 2: press Enter to send each command")
    parser.add_argument("--host", default=host)
    parser.add_argument("--port", type=int, default=port)
    parser.add_argument("--auto", action="store_true", help="Run without Enter pauses")
    parser.add_argument("--quiet", action="store_true", help="Hide raw message bytes")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port must be 1-65535")
    return args
