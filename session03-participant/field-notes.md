# Field notes

Record what you recover. Mark each row:

- **given** — supplied in `FRAME_FORMAT.md`
- **observed** — seen in the capture but not yet reproduced
- **validated** — reproduced independently and confirmed against the server

## Command codes

| Action | Request TYPE | Success TYPE | Confidence |
| --- | --- | --- | --- |
| HELLO | `01` | `81` | given |
| PING | `02` | `82` | given |
| Set brightness | | | |
| Read status | | | |

## SET_BRIGHTNESS payload

| Offset | Size | Meaning | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| 0 | | | | |
| 1 | | | | |

Brightness encoding (number you type → first payload byte):

```
encoded = ?
```

Check construction (the bytes after the encoded value):

```
check = ?
```

## STATUS payload

| Offset | Size | Meaning | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| 0 | | | | |
| 1 | | | | |

## Open questions / uncertainty

-
