#!/usr/bin/env python3
import argparse
import socket


def recv_utf8(conn: socket.socket) -> str | None:
    data = conn.recv(4096)
    if not data:
        return None
    return data.decode("utf-8")


def send_utf8(conn: socket.socket, msg: str) -> None:
    conn.sendall((msg + "\n").encode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Host TCP chat server")
    parser.add_argument("--host", required=True, help="Host/Tailscale IP to bind (e.g. 100.x.x.x)")
    parser.add_argument("--port", type=int, default=6767)
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((args.host, args.port))
        server.listen(1)
        print(f"[listening on {args.host}:{args.port}]")
        conn, addr = server.accept()
        print(f"[connected: {addr[0]}:{addr[1]}]")

        with conn:
            try:
                while True:
                    incoming = recv_utf8(conn)
                    if incoming is None:
                        print("[client disconnected]")
                        break

                    print(f"friend: {incoming}")
                    if incoming.strip().lower() == "exit":
                        print("[friend requested exit]")
                        break

                    try:
                        outgoing = input("you: ")
                    except EOFError:
                        outgoing = "exit"
                    send_utf8(conn, outgoing)
                    if outgoing.strip().lower() == "exit":
                        print("[you requested exit]")
                        break
            except KeyboardInterrupt:
                print("\n[interrupted]")
        print("[server closed]")


if __name__ == "__main__":
    main()
