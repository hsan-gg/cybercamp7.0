# Session 4 — Challenge the Assumptions

You can speak the protocol. This session asks a different question: when a device says
an action needs a higher privilege than you have, does the **server** actually enforce
that — or does it just trust the client not to ask? You will find an operation you are
not supposed to run, and prove the server runs it anyway.

## What is in this folder

| File | What it is |
| --- | --- |
| `controller.exe` | The official controller. Run it, and reverse it — it hides more than its menu shows. |
| `PROTOCOL.md` | The envelope and the documented operator commands. |
| `wire.py` | The framing helper (same as Session 3). |
| `workshop.py` | Your starter. Two TODOs, then run the exploit. |
| `finding-template.md` | The one-page finding you submit. |
| `captures/baseline.pcapng` | A normal operator session, for reference. |

## Four kinds of "no" (and one "yes" that matters)

When a request fails, say *why* — they are not the same:

1. **Transport** — the connection dropped or the framing/CRC was bad.
2. **Parser** — the message was malformed.
3. **Application** — well-formed but refused now (wrong state, wrong role).
4. **Policy violation** — it **succeeded** when it should have been refused. ← the finding.

A crash or an error is not a vulnerability. A forbidden action the server **accepts** is.

## The investigation

1. **Run `controller.exe`.** It does self-test, calibrate, read status. Notice `STATUS`
   returns a **role** number — and that it's always the same low number for you.
2. **Reverse `controller.exe`.** The menu is not everything the controller can do. Find
   the command it never advertises — a way to ask the device *what operations exist and
   what role each one needs*.
3. **Enumerate.** Send that command. One operation needs a **higher role** than you have.
   That's the operation you are not supposed to run.
4. **Reach it.** It only works from the right state — walk the operator chain
   (`SELF_TEST` → `CALIBRATE`) to get there. The server's error messages guide you.
5. **Try it anyway, as your low role.** If the server performs it, you have a verified
   authorization flaw — and it returns a flag.

## Your task

1. Fill the two TODOs in `workshop.py` (the hidden command, and the operation it says you
   are not allowed to use).
2. Run it: enumerate, reach the right state, and send the privileged operation **as your
   low role**. If the server runs it, capture the **flag** it returns.
3. Reproduce it on a fresh connection (it is repeatable, not a fluke).
4. Write the finding in `finding-template.md`: the intended policy you discovered, the
   exact sequence, the result (flag), the root cause, and a fix.

## Deliverables

- The **flag** and a completed `finding-template.md`.
- A short state diagram of the device.
- The reproduced exchange (your `workshop.py` output, or a capture).

## Notes

- Your instructor supplies the server host and port.
- Inspecting and reversing `controller.exe` is expected and allowed.
- You never become the higher role and you never need its credentials — the point is that
  the server lets your low role do the privileged thing.
