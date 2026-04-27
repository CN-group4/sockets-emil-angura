# Tailscale TCP Chat (Mission A, Port 6767)

Simple two-peer TCP chat for class demo:
- **Host** runs the Python server
- **Friend** runs the Java client
- Uses Tailscale network connectivity

## Requirements
- Python 3.8+
- Both devices logged into the same Tailscale tailnet

## Run

### 1) Host machine
Find your Tailscale IP:
```bash
tailscale ip -4
```

Start server on port 6767:
```bash
python3 server.py --host <HOST_TAILSCALE_IP> --port 6767
```

### 2) Friend machine (Java client)
Connect using host Tailscale IP and port `6767`.

Reference Python client (optional, local testing only):
```bash
python3 client.py <HOST_TAILSCALE_IP> --port 6767
```

## TCP protocol contract (Python server ↔ Java client)
- Encoding: **UTF-8** for both send and receive.
- Flow: **sequential ping-pong**.
  - Client sends first message.
  - Server reads and responds.
  - Repeat until one side sends `exit`.
- Stop condition: if either side sends `exit`, both sides close sockets gracefully.
- Message unit: one send/receive per turn (demo-sized messages, up to 4096 bytes).

## Tailscale notes
- Both users must be in the same tailnet and allowed by ACL policy.
- Port `6767/tcp` must not be blocked by local host firewall rules.

## Scope
- This repo currently covers **Mission A (TCP)**.
- Mission B (UDP) is intentionally deferred.

## Prompt for friend AI (Java client)

```text
Build a Java TCP client that interoperates with my Python server for a networking lab.

Server/protocol requirements (must match exactly):
- Connect to host IP (Tailscale IP) and port 6767
- TCP only
- UTF-8 encoding for send/receive
- Sequential ping-pong flow:
  1) Client sends first message
  2) Client waits for server response
  3) Repeat
- If either side sends "exit", close gracefully (socket + streams) and terminate
- Print clear console logs for connection, sent message, received message, disconnect, and exit reason

Implementation constraints:
- Java 17+
- Single-file CLI app named `Client.java`
- Run as: `java Client <HOST_IP> <PORT>`
- Use BufferedReader for console input
- Use InputStreamReader/OutputStreamWriter with explicit UTF-8
- Flush output after every sent message
- Handle connection errors cleanly (host unreachable, refused, broken pipe, EOF)

Deliverables:
1) Full `Client.java` code
2) Short run instructions
3) A tiny compatibility checklist proving it matches:
   - UTF-8
   - client sends first
   - ping-pong turn order
   - exit behavior
4) Optional: small debug flag to print raw bytes length per message

Do not implement server code. Only the Java client.
```
