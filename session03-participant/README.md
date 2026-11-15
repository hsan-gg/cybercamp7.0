# Session 3 — Investigate the Unknown

A laboratory lamp lost its documentation. You have the controller that drives
it, a capture of it working, and the outer message format. You do **not** have
the application rules: which command sets brightness, how the value is encoded,
or how the extra check byte is built. Recover them, then prove you understand
them by driving the lamp from your own Python.

## What is in this folder

| File | What it is |
| --- | --- |
| `controller.exe` | The native lamp controller. Run it, and reverse it in Ghidra. |
| `FRAME_FORMAT.md` | The outer envelope and the HELLO/PING commands you already know. |
| `wire.py` | Generic framing helper (envelope + CRC only). |
| `workshop.py` | Your starter. Four TODOs to fill from what you recover. |
| `teach.c` | A small, separate example program to read first (not the lamp). |
| `teach.exe` | `teach.c` already compiled — open this in Ghidra (no compiler needed). |
| `field-notes.md` | Where you record the fields, with evidence and confidence. |
| `captures/investigation.pcapng` | A recording of the controller in use. |
| `captures/actions.md` | The exact actions and values behind that capture. |

## Tools

- **Wireshark** — read the capture, and record your own.
- **Ghidra** — inspect `controller.exe`: Strings, the Listing, and the Decompiler.
- **Python** — `wire.py`, `struct`, `binascii`, and your `workshop.py`.

## The investigation loop

1. **Run and capture.** Start Wireshark, run `controller.exe`, and drive it:
   set brightness **20 twice**, then **50** and **80**, reading status in
   between. Record your actions.
2. **Compare.** Line up the SET_BRIGHTNESS messages. Which bytes change with the
   value? Which byte(s) change even when you send the *same* value twice?
   Separate SEQ and CRC from the payload.
3. **Reverse.** In Ghidra, find the string `Brightness (0-100):`, follow its
   reference into the function that builds the request, and read the two small
   functions it calls: one turns your number into a byte, one builds the check.
4. **Port.** Reproduce both in `workshop.py` (TODOs 2 and 3), plus the two
   command codes (TODO 1) and the STATUS layout (TODO 4).
5. **Prove it.** Run `workshop.py` to set brightness **60** — a value absent
   from the supplied capture — and confirm it through STATUS.

## Capture it yourself (a recording is included as a fallback)

`captures/investigation.pcapng` is provided so you are never blocked, but you
should record your own:

1. Open Wireshark and select the **Npcap "Adapter for loopback traffic"** (or the
   Wi-Fi interface, for the room). Set the display filter `tcp.port == 9003`.
2. Start the capture **before** you launch the controller.
3. Run `controller.exe` and drive it: set brightness 20 twice, then 50 and 80,
   reading status in between.
4. Stop and save as a `.pcapng`. Use *Follow TCP Stream* to see whole messages.

If live capture does not work (wrong adapter, Npcap not installed), use the
supplied file — it contains the same actions.

## Start here

1. Read `teach.c`, then open the supplied `teach.exe` in Ghidra (compile `teach.c`
   yourself too, if you have a compiler). Find the same three steps there —
   collect values → write a buffer → checksum it — in the decompiler. This is the
   pattern you will meet again inside `controller.exe`.
2. Read `FRAME_FORMAT.md`.
3. Begin the loop above.

## Deliverables

- A completed `field-notes.md` (field table with offsets, meanings, evidence,
  confidence).
- A working `workshop.py` that sets brightness 60 and confirms it.
- One capture showing your independent SET_BRIGHTNESS and the matching STATUS.

## Notes

- Your instructor supplies the server host and port. Run
  `python workshop.py --host <IP> --port <PORT>`.
- Inspecting and reversing `controller.exe` is expected and allowed.
- The check that rides with the brightness is an ordinary application rule, not
  encryption or a password. Treat it as something to understand, not to break.
- The server limits how fast one client may send (about 2 requests/second with a
  short burst). Work at human speed; you will never notice it. Do not script
  floods of requests — ordinary protocol mistakes are fine and never penalized.
