# Task 3 — ECHO Vault (hard, 600 points incl. report)

A laboratory's connected vault supports diagnostics and resumable maintenance sessions. The
ordinary controller can check the device and save a reconnect ticket, but it never offers an
unlock. Recover the protocol, reach a protected operation you are not supposed to use, and
demonstrate it — with a reproducible report.

This task uses only skills from the four sessions. Nothing is handed to you about the wire
format: the captures and `controller.exe` are your sources.

## Scope

- Your sessions run at the ordinary (observer) privilege. The **unlock path requires a higher
  role you are not given.**
- No cryptography is broken, no server key is recovered, no identifiers are brute-forced, and
  no memory corruption is used. The flaw is a logic/trust mistake.

## What is in this folder

| File | What it is |
| --- | --- |
| `controller.exe` | The observer controller. Run it, and reverse it. |
| `crc_helper.py` | The checksum primitives, with documented parameters. |
| `starter.py` | A scaffold. You recover the wire format and build the client. |
| `report-template.md` | The report you submit. |
| `captures/observer-1.pcapng`, `observer-2.pcapng` | Two legitimate observer sessions. |
| `captures/actions.md` | What the captures are. |

## The challenge

1. **Recover the protocol** — the frame, the session handshake, and the operations — from the
   captures and the controller.
2. **Build a working client** that completes the handshake and performs the ordinary
   operations.
3. **Find the operation you are not allowed to run**, and investigate whether the server truly
   stops you, or only the client does.
4. **Reach it and unlock.** A successful unlock returns the **flag**. Your client must work
   with fresh values each run, not replay captured bytes.

## Deliverables

- The **flag** and a 4–6 page report (`report-template.md`): your protocol map, how the
  handshake and its proof work, the root cause of the flaw, reproduction steps, and your
  investigation evidence (including failed hypotheses and negative controls). A flag alone
  earns only part of the score; the report is most of it.

## Notes

- Your instructor supplies the endpoint (host/port).
- Reversing `controller.exe` and inspecting the captures is expected.
- Hints are available (3, costing 5/10/15 points, from this task only).
- A shared board may be available for a physical demonstration in a scheduled slot; software
  success earns the same points.
