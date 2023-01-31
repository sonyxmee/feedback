from imaplib import IMAP4_SSL
import os

import socket
from dotenv import load_dotenv
from multiprocessing import Queue
import email  # для получения заголовков и тела писем
from time import sleep
import logging

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_HOST = os.getenv('IMAP_HOST')
IMAP_PORT = os.getenv('IMAP_PORT')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT')
PERIOD_CHECK = int(os.getenv('PERIOD_CHECK'))

HOST_COLLECTOR = '127.0.0.1'
PORT_COLLECTOR = 50008

IDs = Queue()

with IMAP4_SSL(IMAP_HOST, IMAP_PORT) as M:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST_COLLECTOR, PORT_COLLECTOR))
    s.listen(1)
    conn, address = s.accept()
    rc, resp = M.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    while True:
        data = conn.recv(1024)
        IDs.put(data.decode())
        M.select()  # Returned data is the count of messages in mailbox (список писем)
        status, search_data = M.search(None, 'ALL')
        # search_data - храним найденные почтовые сообщения
        msgs = search_data[0].split()  # массив номеров писем
        print("Found", len(msgs), "messages")
        for num in msgs:
            # fetch - получение информации о письме
            typ, data = M.fetch(num, '(RFC822)')  # Формат почтового сообщения (RFC-822)
            raw_email = data[0][1]  # заносим необработанное письмо
            email_message = email.message_from_bytes(raw_email)  # получаем заголовки и тело письма и заносим результат

            if email_message['Subject'] == IDs.get():
                logging.basicConfig(filename="success_request.log", level=logging.INFO)
                logging.info(email_message['Subject'])
                body = email_message.get_payload(decode=True).decode('utf-8')  # вывод содержимого письма
                logging.info(body)
            else:
                logging.basicConfig(filename="error_request.log", level=logging.INFO)
                body = email_message.get_payload(decode=True).decode('utf-8')
                logging.error(body)
            """body = email_message.get_payload()[0].get_payload(decode=True).decode('utf-8')
            subject = int(email_message['Subject'])

            if email_message['Subject'] == IDs.get():
                log = open("success_request.log", "a")
            else:
                log = open("error_request.log", "a")
            log.write("%s: %s\n" % (subject, body))
            log.close()"""
        sleep(PERIOD_CHECK)
