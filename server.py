import socket
import random
from smtplib import SMTP
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(""), '.env')
load_dotenv(dotenv_path)
EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_HOST = os.getenv('IMAP_HOST')
IMAP_PORT = os.getenv('IMAP_PORT')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT')
PERIOD_CHECK = os.getenv('PERIOD_CHECK')
username = 'forpython024@gmail.com'
password = 'minibika13'

HOST = '127.0.0.1'
PORT = 12345
HOST_COLLECTOR = '127.0.0.1'
PORT_COLLECTOR = 50008

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # привязка сокета к адресу
    s.listen(5) # сервер может подключать данные, 5-кол-во подключений, кот. будут ждать
    user_socket, address = s.accept() # принятие данных
    with user_socket:
        print('Connected by', address)
        while True:
            email = user_socket.recv(1024)
            msg = user_socket.recv(2048)

            if not email:
                break
            if (not email) or (not msg):
                break
            if '@' not in email.decode("utf-8"):
                user_socket.sendall(b'Wrong email format')
                continue

            ID = email.decode() + str(random.getrandbits(10))  # Уникальный ID
            with SMTP(SMTP_HOST, SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(username, password)
                BODY = "\r\n".join((
                    "From: %s" % EMAIL_LOGIN,
                    "To: %s" % EMAIL_LOGIN,
                    "Subject: %s" % ID,
                    "",
                    msg.decode("utf-8")
                ))
                smtp.sendmail(
                    EMAIL_LOGIN,
                    EMAIL_LOGIN,
                    BODY
                )
                BODY = "\r\n".join((
                    "From: %s" % EMAIL_LOGIN,
                    "To: %s" % email.decode(),
                    "Subject: %s" % ID,
                    ""
                ))
                smtp.sendmail(
                    EMAIL_LOGIN,
                    email.decode(),
                    BODY
                )
                user_socket.sendall(b'OK')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
                c.connect((HOST_COLLECTOR, PORT_COLLECTOR))
                c.sendall(bytes(ID, 'utf-8'))

            user_socket, address = s.accept()
