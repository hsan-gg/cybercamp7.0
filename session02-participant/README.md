# Session 2: Speak the protocol

## 1. Use the controller

Extract the entire ZIP, then **double-click controller.exe**. Enter the target IP and port supplied by your instructor and click Connect. You do not need Python installed to run this Windows x64 controller.

Start Wireshark before connecting. Capture on Wi-Fi for a remote target, or loopback when the server runs on your own machine. Filter with `tcp.port == 9001`, using your assigned port.

Try **Ping → LED On → Read Status → LED Off → Read Status**. The Cybercamp controller is the same app used in Session 1, with the workshop's purple/cyan colors and Securinets logo. Its device panel shows the target's LED acknowledgment/status and simulated temperature. Enable **Show message bytes** to compare TX/RX bytes; turning it on also reveals earlier messages from the current log. These counters count application messages, not TCP packets. Inspecting or reversing the controller is allowed.

## 2. Write your own messages

Open **workshop.py**. There are two TODOs:

1. Finish `build_message()`: pack the header, calculate CRC, append the payload and CRC bytes. The field specification is in `PROTOCOL.md`; the CRC helper call is supplied in comments.
2. After the existing HELLO/PING, add SET_LED ON and STATUS, then SET_LED OFF and STATUS. Check acknowledgments and verify the returned LED state each time.

Receiving, partial TCP reads, response checks, and status decoding are provided in `workshop_helpers.py` and `protocol.py`. Keep both beside your script. You can inspect them, but you do not need to rewrite that plumbing during the exercise.

Edit HOST/PORT at the top of workshop.py, or run:

```powershell
python workshop.py --host TARGET_IP --port 9001
```

Python 3.9+ is needed for this script; no pip packages are required. **Press Enter before each command.** Stop to inspect the capture and discuss the result. The starter reports a TODO until you complete it. Use `--auto` only when you want all messages sent without pauses.

Check your encoder with SET_LED ON and request identifier 3:

```text
CA FE 01 04 03 00 01 00 01 CD 86
```

The target allows roughly ten minutes of inactivity. Reconnect after a longer pause. Use `127.0.0.1` only when the server is on your own laptop. Your instructor may assign the Pico W endpoint later: the same script controls its physical onboard LED. Temperature remains simulated.

## 3. Show your result

Provide your completed Python script, a saved `.pcapng`, and one annotated request/response. Identify TYPE, SEQ, LENGTH, payload, and CRC coverage. Explain why a valid CRC does not authenticate a sender.

The saved `captures/session02-practice.pcapng` is a fallback if live capture fails. There is no competition flag in this training exercise. Another team on the same target can change its LED, so use your assigned endpoint.
