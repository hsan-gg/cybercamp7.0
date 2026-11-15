"""Complete two TODOs. This is named workshop.py in the participant ZIP."""

import binascii
import socket
import struct

from workshop_helpers import decode_status, parse_target, receive_reply

HOST, PORT = "127.0.0.1", 9001  # Replace HOST with the instructor's target IP.
HELLO, PING, STATUS, SET_LED = 1, 2, 3, 4


def build_message(command, sequence, payload=b""):
    # TODO 1: pack the header, calculate CRC, return header + payload + CRC bytes.
    # Header: struct.pack('<2sBBHH', magic, version, command, sequence, payload_length)
    # CRC: binascii.crc_hqx(header[2:] + payload, 0xFFFF); store with '<H'.
    header = struct.pack("<2sBBHH", b"\xca\xfe", 1, command, sequence, len(payload))
    crc = binascii.crc_hqx(header[2:] + payload, 0xFFFF)
    return header + payload + struct.pack("<H", crc)
    if len(payload) > 256:
        raise ValueError("Payload exceeds 256 bytes")
    raise NotImplementedError("TODO 1: build the message")


def run(host, port, pause=input):
    with socket.create_connection((host, port), timeout=5) as sock:

        def send(command, sequence, payload=b""):
            if pause:
                pause(
                    "\nPress Enter to send command %02x (request %d)..."
                    % (command, sequence)
                )
            message = build_message(command, sequence, payload)
            print("TX", message.hex(" "))
            sock.sendall(message)
            return receive_reply(sock, command, sequence)

        print("Device:", send(HELLO, 1).decode("ascii"))
        if send(PING, 2) != b"PONG":
            raise ValueError("Expected PONG")
        print("PONG received")
        # TODO 2: send(SET_LED, 3, b'\x01'), then decode_status(send(STATUS, 4)).
        # Confirm LED == 1. Repeat with OFF (b'\x00') and request identifiers 5/6.
        # Verify both SET_LED replies equal the requested one-byte value.
        send(SET_LED, 3, b"\x01")
        decode_status(send(STATUS, 4))
        raise NotImplementedError("TODO 2: turn the LED ON/OFF and verify each STATUS")


if __name__ == "__main__":
    args = parse_target(HOST, PORT)
    try:
        run(args.host, args.port, None if args.auto else input)
    except (
        OSError,
        EOFError,
        ValueError,
        NotImplementedError,
        KeyboardInterrupt,
    ) as error:
        print("Stopped:", error)
        raise SystemExit(1)
