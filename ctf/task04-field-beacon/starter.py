"""Field Beacon starter (participant).

The datagram format is NOT given. Recover it from the capture and tool.exe, then reach the
maintenance query the tool never sends.

Run: python starter.py --host <ip> --port <port>
"""
import argparse
import socket


# TODO 1 — the datagram format.
#   From the capture and tool.exe (its checksum function), work out the header fields, their
#   order and sizes, and the 2-byte integrity check at the end (what it covers, which
#   function). Write build(opcode, req_id, payload) and parse(reply).

# TODO 2 — the maintenance query.
#   Reverse tool.exe to find the opcode it hides. Build a datagram for it with a VALID check,
#   send it over UDP, and read the flag from the reply. (A valid check is all the device
#   asks for -- is that really a permission?)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9006)
    parser.parse_args()
    # UDP: socket.socket(AF_INET, SOCK_DGRAM); sendto((host, port)); recvfrom(2048)
    raise SystemExit("Build the UDP client from the capture and tool.exe (see the TODOs).")


if __name__ == "__main__":
    main()
