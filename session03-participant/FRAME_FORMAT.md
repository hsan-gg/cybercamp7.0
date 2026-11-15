# Lamp protocol — what you are given

The lamp speaks over TCP using the **same outer envelope you built in Session 2**.
That part is supplied. What each application command means, and how its payload
is built, is what you investigate.

## Outer message

```
MAGIC(2) | VERSION(1) | TYPE(1) | SEQ(2 LE) | LENGTH(2 LE) | PAYLOAD(N) | CRC16(2 LE)
```

| Offset | Size | Field | Value |
| --- | --- | --- | --- |
| 0 | 2 | MAGIC | `CA FE` |
| 2 | 1 | VERSION | `01` |
| 3 | 1 | TYPE | application command or response code |
| 4 | 2 | SEQ | request identifier, little-endian, +1 per request |
| 6 | 2 | LENGTH | payload length, little-endian, max 256 |
| 8 | N | PAYLOAD | command-specific (you recover this) |
| 8+N | 2 | CRC16 | little-endian |

- **CRC16** is CRC-16/CCITT-FALSE (poly `0x1021`, init `0xFFFF`, no reflection,
  final XOR 0), computed over VERSION through the end of PAYLOAD — exactly the
  Session 2 rule. The supplied `wire.py` already does this for you.
- A complete message is `10 + N` bytes.
- A **successful** reply uses `TYPE | 0x80` and echoes the request's SEQ.
- An **error** reply uses TYPE `FF` with a short UTF-8 message. The connection
  stays usable after an application error; only bad framing/CRC closes it.

## Commands you already know

| Action | Request TYPE | Request payload | Success TYPE | Success payload |
| --- | --- | --- | --- | --- |
| HELLO | `01` | empty | `81` | the device name, then a **4-byte session value** (little-endian) |
| PING | `02` | empty | `82` | `PONG` |

The 4-byte value at the end of the HELLO reply is fresh for every connection.
Keep it — one of the other commands needs it.

## Commands you must recover

There are two more TYPEs in the traffic. One sets the brightness; one reads the
status. Their codes, payload layout, the value transformation, and the extra
check that rides along with the brightness are the investigation. Record what
you find in `field-notes.md`.

## `wire.py` helper

```python
from wire import encode, receive, Frame, crc16, ProtocolError

encode(opcode, sequence, payload=b"")   # -> complete message bytes
receive(sock)                           # -> Frame(opcode, sequence, payload)
```

`wire.py` only knows the envelope and CRC. It does not know the command codes,
the brightness encoding, or the check. That is the point.
