# Security finding

**Team:**
**Target:** Session 4 lamp, `<host>:<port>`

## Summary

One or two sentences: what is the flaw and what can an operator do?

## Intended policy

What the device is supposed to enforce (quote `PROTOCOL.md`).

## Steps to reproduce

The exact sequence you sent, as an operator:

1. HELLO
2. STATUS → state =        , role =
3. OVERDRIVE from READY → result:
4. SELF_TEST → test_id =
5. CALIBRATE(test_id) → calib_id =
6. OVERDRIVE(calib_id) → result:
7. STATUS → state =        , brightness =

## Observed result

What happened at step 6, and how step 7 confirms it (the state/output change).

## Why it is a flaw (root cause)

Which check the server performs, and which it is missing. Distinguish the state
check (present) from the role check (missing).

## Negative controls

- OVERDRIVE from the wrong state → (expected: rejected, proves a state check exists)
- OVERDRIVE on a fresh connection with an old id → (expected: rejected)

## Fix

What the corrected handler must check, and why hiding the button in the client or
adding another checksum would not fix it.
