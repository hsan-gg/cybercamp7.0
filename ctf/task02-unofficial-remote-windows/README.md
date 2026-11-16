# The Unofficial Remote

**Difficulty:** medium. **Points:** 250.

This laboratory instrument accepts profile changes through an undocumented TCP
protocol. Ordinary operators may select ECO, NORMAL, and TURBO. Maintenance mode
is reserved for service personnel and must not be available to ordinary operators.

The supplied controller permits only ordinary profiles. Investigate whether the
instrument itself enforces the same restriction. Write a Python client that
demonstrates the result and submit the returned `CCW{...}` flag.

You receive:

- A native controller executable; inspecting or reverse engineering it is allowed.
- `normal-session.pcapng`, recorded while the ordinary controller was used.
- `crc_helper.py`, providing the checksum primitive and its exact parameters.
- A live target address and TCP port, assigned by the organizer.

On Windows, open PowerShell in this folder and run:

```powershell
.\controller.exe 127.0.0.1 9201
```

Replace the example address/port with your assigned endpoint. The controller
offers status, profile listing, and profile selection. Idle sessions close after
two minutes; restart the controller if necessary. The normal controller has no
flag or server credentials embedded in it.

On Linux/macOS use an organizer-provided native `controller` build. The current
Windows executable is not a Linux binary; ask the organizer for the appropriate
build before the event.

For a live connection to another machine, capture on your active Wi-Fi/Ethernet
interface. For a target on your own machine at `127.0.0.1`, capture on loopback.
Example display filter: `tcp.port == 9201`. The supplied capture uses loopback
addresses and has two separate TCP streams. Inspect the reassembled application
data as well as individual packets.

No hardware is needed. Do not scan or interfere with other teams' targets.

