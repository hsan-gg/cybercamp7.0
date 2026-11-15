# Session 2 teaching protocol, version 1

This specification is intentionally public for the guided client-building lab. It is wire-compatible with the existing `controller_demo` and Session 1 practice capture. It is not a competition protocol or the deferred ECHO Vault challenge.

Transport: plain TCP, default server port **9001**. Start a new connection with HELLO. Discovery is not implemented; enter the assigned endpoint. A server response uses the same frame format as a request.

| Offset | Size | Field | Interpretation |
| --- | --- | --- | --- |
| 0 | 2 | MAGIC | Literal bytes `CA FE` |
| 2 | 1 | VERSION | `01` |
| 3 | 1 | TYPE | Command or response code |
| 4 | 2 | SEQ | Unsigned little-endian request identifier; response echoes it |
| 6 | 2 | LENGTH | Unsigned little-endian payload byte count, **0–256** |
| 8 | N | PAYLOAD | Command-specific bytes |
| 8+N | 2 | CRC16 | Unsigned checksum stored little-endian |

Header size: 8 bytes (`<2sBBHH`). Complete message size: `10 + LENGTH`. TCP segment boundaries and `recv()` return boundaries do not delimit messages. Read the complete header, validate it, then read the bounded payload and two-byte CRC. Adjacent messages can arrive in a single TCP read.

## Checksum

CRC-16/CCITT-FALSE (also called CRC-16/IBM-3740): width 16, polynomial `0x1021`, initial value `0xFFFF`, no input/output reflection, final XOR `0x0000`. Calculate over **VERSION through PAYLOAD**, excluding MAGIC and the CRC itself. Store the result little-endian. Check vector: ASCII `123456789` produces `0x29B1`.

```python
crc = binascii.crc_hqx(header[2:] + payload, 0xFFFF)
crc_bytes = struct.pack('<H', crc)
```

Example SET_LED ON, request identifier 3:

```text
CA FE | 01 | 04 | 03 00 | 01 00 | 01 | CD 86
MAGIC   V   TYPE   SEQ   LENGTH   DATA  CRC
```

The CRC detects accidental corruption. It contains no secret and authenticates neither the sender nor the operation.

## Commands

| Command | Request TYPE | Request payload | Success TYPE | Success payload |
| --- | --- | --- | --- | --- |
| HELLO | `01` | Empty | `81` | ASCII device name, 1–64 bytes |
| PING | `02` | Empty | `82` | ASCII `PONG` |
| STATUS | `03` | Empty | `83` | Three bytes: LED state + signed little-endian int16 temperature |
| SET_LED | `04` | Exactly `00` or `01` | `84` | Echo of the one-byte LED value |

Success TYPE is `request_type | 0x80`. The SEQ is an application identifier, unrelated to TCP sequence numbers. The reference clients increment it modulo 65536. The server echoes it but does not enforce monotonicity, uniqueness, authorization, or replay protection.

Temperature is **simulated** at 2375 hundredths of a degree C (23.75 C) in both implementations. STATUS payload `01 47 09` means LED ON and 23.75 C. Decode with `struct.unpack('<Bh', payload)` and divide temperature by 100.

HELLO establishes only application readiness; it does not authenticate a user. A repeated valid HELLO is permitted. Greeting state is per TCP connection. LED state is shared by everyone connected to one target instance and remains set across reconnects until changed or the process/board is reset.

## Rejections and connection handling

- Well-framed invalid requests return TYPE `FF`, the echoed SEQ, and a UTF-8 explanation. The connection remains usable.
- Before successful HELLO, other commands return `Send HELLO first`.
- Empty-payload commands reject non-empty payloads. SET_LED rejects payloads other than exactly one byte `00` or `01`. Unknown commands return `Unknown command` after HELLO.
- Bad magic/version, oversized length, invalid CRC, or a truncated message closes/resets the connection. No `FF` reply is promised for malformed frames.
- The Python simulator closes after a ten-minute receive timeout. The board uses a roughly ten-minute no-input timeout, checked periodically. Slow partial-input timing can differ; do not use either as an internet-facing production service.
- Treat EOF and TCP reset as connection termination. Reconnect and send HELLO again.
- Validate responses too: header/CRC, SEQ, success/error TYPE, payload size, and permitted values. Read STATUS to corroborate a requested state change.

## Hardware and simulator

The Pico W joins a WPA2-capable **2.4 GHz** router network as a station; it does not act as the workshop access point. The onboard LED is controlled through the CYW43 API. The firmware supports four bounded client slots and a bounded output queue; excess clients or output overload may be reset. Schedule one team at a time for physical validation. The simulator supports parallel participant work; one process/port per team avoids conflicting LED actions.
