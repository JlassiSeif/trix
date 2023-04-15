import socket
import time
from src.deck import deck
from src.logic import Logic

MAX_CLIENTS = 1
client_fds = []


def main():
    global client_fds
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("0.0.0.0", 8080))
    server_sock.listen(MAX_CLIENTS)
    print("Server listening on port 8080...")

    while len(client_fds) < MAX_CLIENTS:
        client_sock, address = server_sock.accept()
        print(f"Client {client_sock} connected")
        client_fds.append(client_sock)
    time.sleep(1)
    names = ["lam3i", "bochra", "ldhaw", "klafez"]
    for i, fd in enumerate(client_fds):
        message = f"{names[i]},{i}"
        client_fds[i].send(message.encode())

    time.sleep(1)
    end_game = False
    l = Logic(client_fds)
    while not end_game and len(client_fds) == MAX_CLIENTS:
        end_game = l.step()

    # for fd in client_fds:
    #     message = "disconnect"
    #     client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     client_sock.connect(("127.0.0.1", 8080))
    #     client_sock.sendall(message.encode())
    #     client_sock.close()

    time.sleep(1)
    server_sock.close()


if __name__ == "__main__":
    main()
