import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print("\n📩", message)
        except:
            print("Соединение разорвано")
            sock.close()
            break

def send_messages(sock):
    while True:
        message = input()
        try:
            sock.send(message.encode())
        except:
            break

def start_client():
    server_ip = input("Введите IP сервера: ")
    port = int(input("Введите порт: "))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, port))
    except:
        print("Не удалось подключиться")
        return

    print("Подключено к серверу")

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    # Основной поток — отправка
    send_messages(client)

if __name__ == "__main__":
    start_client()
