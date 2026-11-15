# Cybercamp — Session 1: Observe the conversation

Use a working application, capture its conversation, and explain one request and
reply. You will implement your own Python client in Session 2.

## What you receive

- `controller.exe`: the shared Sessions 1/2 controller, ready to run on Windows x64.
- The server IP and TCP port, supplied by your instructor.
- `captures/session01-practice.pcapng`: a fallback recording if live capture fails.

Install and test Wireshark/Npcap before the workshop. The controller bundles its
runtime; Python is not required to run it. Its purple/cyan interface includes the
Securinets logo, connection status, device state, and conversation log.

## 1. Capture your own conversation

1. Join the workshop Wi-Fi. Internet access is unnecessary.
2. Open Wireshark and select your Wi-Fi interface.
3. Start capturing **before** clicking Connect in the controller.
4. Enter the assigned server IP and port, then click Connect.
5. Click **Ping → LED On → Read Status → LED Off → Read Status**.
6. Click Disconnect, stop capturing, and save `your-name-session01.pcapng`.

If both programs run on your own machine at `127.0.0.1`, capture the Npcap loopback
interface instead. Each participant captures their own controller/server traffic;
Wi-Fi monitor mode is unnecessary.

Apply the display filter below, substituting the assigned port if needed:

```text
tcp.port == 9001
```

## 2. Follow the exchange

With your instructor, identify:

- Client/server IP addresses and ports; who initiates the connection.
- The TCP connection setup and an ACK with no application payload.
- One request and its application reply.
- The application bytes in the packet details and byte pane.

Right-click an application packet and choose **Follow → TCP Stream**, then choose
**Hex Dump**. Compare both directions. The controller's **Show message bytes**
checkbox provides another view of the same application bytes; it is not a packet
capture. Its TX/RX counters count application messages.

## 3. Read one message

Annotate a request and reply with the instructor's field map. Locate the command,
request identifier, payload length, value byte, and CRC. Compare LED ON and OFF:
the value changes, and the identifier/CRC may change too. A CRC detects changes
to the covered bytes; it does not authenticate the sender.

Your live capture's frame numbers may differ from the fallback. In the supplied
sample, frames 12/14 are an LED ON request/reply and frames 8/10 are PING/PONG.
The fallback was recorded over loopback, so its addresses differ from the venue.
Temperature is simulated; LED state is software when using the laptop simulator.

## Your deliverable

Save your `.pcapng` and annotate **one request/reply pair**: frame numbers,
endpoints, direction, and relevant application bytes. No Python implementation
is required in Session 1. Keep the controller for Session 2.
