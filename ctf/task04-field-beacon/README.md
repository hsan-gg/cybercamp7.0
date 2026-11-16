# Task — Field Beacon (medium, 250 points)

A field sensor module answers queries over **UDP**. The operator tool reads its status and a
sensor value. There is also a maintenance query the tool never sends — it returns a `CCW{...}`
flag. Recover the protocol, reach that query, and submit the flag.

Nothing about the wire format is handed to you: the capture and `tool.exe` are your sources.

## Scope

- This is a **connectionless UDP** protocol: one datagram per message, no handshake, no session.
- Ordinary queries work for anyone. The maintenance query is meant for service tools only —
  the operator tool does not offer it. Investigate whether the device really keeps it reserved.
- No cryptography is broken and no hardware is needed. The flaw is a logic/trust mistake.

## What is in this folder

| File | What it is |
| --- | --- |
| `tool.exe` | The operator tool. Run it, and reverse it. |
| `starter.py` | A scaffold. You recover the datagram format and build the client. |
| `captures/beacon.pcapng` | A normal operator session (status and sensor reads). |
| `captures/actions.md` | What the capture is. |

## The challenge

1. **Recover the datagram format** from the capture and the tool: the header fields, and the
   **2-byte integrity check** at the end of every datagram (recover the exact function — it is
   in `tool.exe`).
2. **Build a UDP client** that sends a valid status query and reads the reply.
3. **Find the maintenance query** the tool hides (reverse `tool.exe`), and ask whether the
   device's integrity check is actually a permission check.
4. **Send the maintenance query yourself**, with a valid integrity check. If the device answers
   it, you get the **flag**.

## Deliverable

- The **flag**. Keep short notes (which query, how you computed the check, how you found the
  maintenance opcode) for the debrief.

## Notes

- Your instructor supplies the endpoint (host/port). It is UDP — in Wireshark capture on the
  interface the traffic uses (loopback for a local target), filter on the UDP port.
- Reversing `tool.exe` and inspecting the capture is expected.
- Hints are available (3, costing 5/10/15 points, from this task only).
