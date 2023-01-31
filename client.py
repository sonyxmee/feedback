import socket

HOST = '127.0.0.1'
PORT = 12345
while True:
    email = input("Input your email: ")
    msg = input("Input your message: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # связываем клиента с сервером
        s.send(email.encode("utf-8"))
        s.send(msg.encode("utf-8"))
        data = s.recv(1024).decode("utf-8")  # 1024-сколько в одном пакете байт
        if data == "OK":
            print("Success!")
            exit()
        else:
            print("Ошибка: ", repr(data), "\n")  # repr() msg about error
            print("Введите данные еще раз!\n")
