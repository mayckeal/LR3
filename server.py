import socket
import threading

clients = {}
# {socket: username}

def broadcast(message, sender=None):
    for client in list(clients.keys()):
        if client != sender:
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"[-] {username} отключился")

        broadcast(f" {username} вышел из чата")

        del clients[client_socket]
        client_socket.close()

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode()
        clients[client_socket] = username

        print(f"[+] {username} подключился")
        broadcast(f" {username} вошёл в чат")

        while True:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            if message == "/exit":
                break

            print(f"{username}: {message}")
            broadcast(f"{username}: {message}", client_socket)

    except:
        pass

    remove_client(client_socket)

def start_server():
    host = input("Введите IP сервера: ")
    port = int(input("Введите порт: "))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
    except OSError:
        print("Порт уже занят!")
        return

    server.listen()
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
