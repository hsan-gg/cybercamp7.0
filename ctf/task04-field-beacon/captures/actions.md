# Capture notes

A recording of the **operator tool** talking to the beacon over **UDP**, loopback.
Filter on the UDP port. Each datagram is one complete message (UDP preserves boundaries).

The capture contains only ordinary queries — status and sensor reads — and their replies.
There is no maintenance query and no flag here; that is for you to reach.

Use it to confirm the datagram format and to **check your recovered integrity function**: the
last two bytes of every datagram are its check, so once you think you know the function, verify
it reproduces those bytes for the datagrams you see.
