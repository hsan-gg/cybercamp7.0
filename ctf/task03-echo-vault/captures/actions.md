# Capture notes

Two recordings of the **observer** controller against the vault, loopback TCP.
Filter on the server port and Follow TCP Stream to read whole messages.

Each capture is one ordinary observer session: connect, run the observer actions the
controller offers, and reconnect once. Neither capture contains any privileged operation or a
flag — those are for you to reach.

## Why two captures

The two sessions are **not identical**. Compare them byte for byte: what is fixed, what is
fresh each session, and what arrives in a different order. Those differences tell you how the
session is bound, what you could replay, and what you could not.
