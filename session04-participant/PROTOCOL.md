# Lamp protocol — Session 4 (what you are given)

Same outer envelope as Session 3; `wire.py` handles it. The operator commands below
are documented. The device has **more** than this — finding what, and who is allowed
to use it, is the investigation.

## Outer message

```
MAGIC(2)=CA FE | VERSION(1)=01 | TYPE(1) | SEQ(2 LE) | LENGTH(2 LE) | PAYLOAD(N) | CRC16(2 LE)
```

Success replies use `TYPE | 0x80` and echo SEQ; errors use `FF` with a short message and
keep the connection open.

## Documented operator commands

| Command | TYPE | Request | Success | Success payload |
| --- | --- | --- | --- | --- |
| HELLO | `01` | empty | `81` | device name |
| STATUS | `10` | empty | `90` | `state(1) role(1) brightness(1)` |
| SELF_TEST | `20` | empty | `A0` | `test_id(4 LE)` |
| CALIBRATE | `21` | `test_id(4 LE)` | `A1` | `calib_id(4 LE)` |

- `STATUS` returns three bytes. The middle one is your **role**, as a number. What the
  numbers mean is for you to work out.
- The operator path is a short chain: `SELF_TEST` then `CALIBRATE`. Each returns an id the
  next step needs; a command sent out of order is rejected.
- A new connection is a fresh session: it starts over, and ids from an old session are
  worthless.

## What is not documented here

The official controller (`controller.exe`) offers only self-test, calibrate, and status.
But the device answers more than those four commands, and some operations may need a role
you do not have. The controller binary is the place to look for what the menu does not
show. When you find a way to ask the device what it can do, use it.

Your job this session is not to recover an algorithm (that was Session 3). It is to find
an operation you are **not supposed** to be able to run, and determine whether the server
actually stops you — or only the client's menu does.
