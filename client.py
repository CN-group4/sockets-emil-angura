#!/usr/bin/env python3
import argparse
import socket


def recv_utf8(sock: socket.socket) -> str | None:
    data = sock.recv(4096)
    if not data:
        return None
    return data.decode("utf-8")


def send_utf8(sock: socket.socket, msg: str) -> None:
    sock.sendall((msg + "\n").encode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Client TCP chat")
    parser.add_argument("server_ip", help="Host Tailscale IP")
    parser.add_argument("--port", type=int, default=6767)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((args.server_ip, args.port))
        except OSError as exc:
            raise SystemExit(f"Connection failed: {exc}") from exc

        print(f"[connected to {args.server_ip}:{args.port}]")
        try:
            while True:
                try:
                    outgoing = input("you: ")
                except EOFError:
                    outgoing = "exit"
                send_utf8(sock, outgoing)
                if outgoing.strip().lower() == "exit":
                    print("[you requested exit]")
                    break

                incoming = recv_utf8(sock)
                if incoming is None:
                    print("[host disconnected]")
                    break

                print(f"host: {incoming}")
                if incoming.strip().lower() == "exit":
                    print("[host requested exit]")
                    break
        except KeyboardInterrupt:
            print("\n[interrupted]")
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        print("[client closed]")


if __name__ == "__main__":
    main()
