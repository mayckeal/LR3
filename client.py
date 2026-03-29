import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            print("Соединение разорвано")
            break

def send_messages(sock):
    while True:
        message = input()

        if message == "/exit":
            sock.send("/exit".encode())
            sock.close()
            print("Вы вышли из чата")
            break

        try:
            sock.send(message.encode())
        except:
            break

def start_client():
    server_ip = input("Введите IP сервера: ")
    port = int(input("Введите порт: "))
    username = input("Введите ваше имя: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, port))
    except:
        print("Не удалось подключиться")
        return

    client.send(username.encode())

    print("Подключено к серверу")
    print("Для выхода напишите /exit")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(client)

if __name__ == "__main__":
    start_client()
