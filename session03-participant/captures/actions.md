# Capture action log — investigation.pcapng

Loopback TCP to the lamp server on port 9003. Brightness **60 is deliberately
absent** — it is the value you will set independently from Python at the end.

Open filter: `tcp.port == 9003`. Follow TCP Stream to see each complete message.
Frame numbers and TCP segmentation can vary between runs; the application
messages below are what matter.

| # | Action | What the controller sent | Why it is here |
| --- | --- | --- | --- |
| 1 | Connect | automatic HELLO | Greeting, and the 4-byte session value in the reply |
| 2 | Ping | PING | A request with no value |
| 3 | Ping again | PING | Same operation — see which header fields change |
| 4 | Set brightness 20 | SET_BRIGHTNESS | One known input/output pair |
| 5 | Read status | READ_STATUS | Corroborate the brightness; note the temperature |
| 6 | Set brightness 20 again | SET_BRIGHTNESS | **Same value, sent again** |
| 7 | Set brightness 50 | SET_BRIGHTNESS | A value-dependent payload byte |
| 8 | Set brightness 80 | SET_BRIGHTNESS | Another value-dependent payload byte |
| 9 | Read status | READ_STATUS | Temperature has moved since action 5 |

## Things worth noticing

- Compare actions **4 and 6**: the same brightness (20) was set twice. The first
  payload byte is identical both times, but the bytes after it are **different**.
  What changed between the two requests, if the value did not?
- Compare the first payload byte across actions 4, 7, 8 (brightness 20, 50, 80).
  Is it the number you typed, or something derived from it?
- Compare the STATUS replies at actions 5 and 9. One field tracks the brightness
  you set. Another field changed on its own. Which is which?

## Example (your capture will differ)

The session value and the check bytes depend on the connection, so your own
numbers will not match these exactly — that is itself a clue.

```
HELLO  reply payload: 53 45 53 53 49 4f 4e 33 2d 4c 41 4d 50 | 60 84 7c a3
                      S  E  S  S  I  O  N  3  -  L  A  M  P   | <-- 4-byte session value (LE)

Set 20 (first time):  payload = 55 d7 73 0f ec
Set 20 (second time): payload = 55 b9 a7 8b ef     <- same first byte, different tail
Set 50:               payload = 6f 3c 14 45 28
Set 80:               payload = 11 3a 0f a4 94

STATUS after 20:      payload = 14 2e 09      -> 14 = 20,  09 2e = 2350 = 23.50 C
STATUS after 80:      payload = 50 33 09      -> 50 = 80,  09 33 = 2355 = 23.55 C
```
