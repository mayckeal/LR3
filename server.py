import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"[+] Подключен: {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"{addr}: {message}")
            broadcast(message, client_socket)
        except:
            break

    print(f"[-] Отключен: {addr}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.remove(client)

def start_server():
    host = input("Введите IP сервера: ")
    port = int(input("Введите порт: "))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Проверка доступности порта
    try:
        server.bind((host, port))
    except OSError:
        print("Порт уже занят!")
        return

    server.listen()
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
