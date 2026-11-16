# ECHO Vault — report

**Team:**
**Target:** `<host>:<port>`  **Flag:**

## 1. Summary
What the flaw is, and what an observer can do with it (2–3 sentences).

## 2. Initial observations
Endpoints, the captures you used, the operations you saw, and your tools.

## 3. Protocol specification
Outer frame offsets, lengths, byte order, CRC coverage; the operation codes; the 36-byte
ticket layout; and an annotated request/response.

## 4. Handshake and state
- TCP setup vs. the application handshake.
- Challenge fragments: index vs. arrival order; how you assemble the server nonce.
- The transcript serialization and the proof (and why the public proof is not authentication).
- SID and the request counter; why an old proof fails on reconnect.
- Roles, calibration/arming, and the state sequence to UNLOCK.

## 5. Investigation narrative
Your hypotheses, the controlled changes you made, relevant packet numbers, and the
native-code / pseudocode evidence for the proof function. Include **negative controls**:
- an old proof replayed on a fresh connection (result?),
- a changed opaque ticket-identifier byte with the tag unchanged (result?),
- the changed role byte with a correctly rebuilt current handshake (result?).
Explain the differing results without claiming you recovered the server key.

## 6. Root cause
What the ticket's authentication tag covers, and what it omits. Why accepting the ticket's
role byte lets an observer act as maintenance.

## 7. Reproduction
Environment, dependencies, the command to run your client, and the full sequence:
fresh session -> observer ticket -> role modification -> reconnect -> calibrate/arm/unlock,
with the expected responses. The script must use fresh values, not hardcoded captured ones.

## 8. Remediation
The fix (authenticate the whole ticket body, including role; keep role/state checks on every
privileged operation; bind the tag to purpose/version/team/device/generation). Explain why an
extra CRC or hiding the UI would not fix it.
