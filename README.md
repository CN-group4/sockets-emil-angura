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
