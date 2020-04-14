#!/usr/bin/env python3

import socket
import ssl
import base64

HOST = "smtp.yandex.ru"
PORT = 587


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to {HOST}, port: {PORT}")
    s.connect((HOST, PORT))
    connect_answer = s.recv(1024)
    print(connect_answer.decode())
    send_and_get_answer(s, b("EHLO x"))
    ans = send_and_get_answer(s, b("STARTTLS"))
    check(220, ans)
    ss = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv23)
    ans = send_and_get_answer(ss, b("AUTH LOGIN"))
    check(334, ans)
    email = input("Your email:\n")
    ans = send_and_get_answer(ss,
                              base64.b64encode(bytes(email, encoding="utf-8")))
    check(334, ans)
    pwd = input("Your password:\n")
    ans = send_and_get_answer(ss, base64.b64encode(bytes(pwd, encoding="utf-8")))
    check(235, ans)
    ans = send_and_get_answer(ss, b(f"MAIL FROM: <{email}>"))
    check(250, ans)
    rcpt_to = input("Recipient address:\n")
    ans = send_and_get_answer(ss, b(f"rcpt to: <{rcpt_to}>"))
    check(250, ans)
    ans = send_and_get_answer(ss, b("DATA"))
    check(354, ans)
    subject = input("Subject:\n")
    text = input("Text:\n")
    data = f"""From: <{email}>
To: <{rcpt_to}>
Subject: {subject}


{text}
."""
    ans = send_and_get_answer(ss, b(data))
    check(250, ans)


def check(code, ans):
    answers = {220: '220 reply not received from server',
               250: '250 wrong address or error while sending',
               334: '334 incorrect answer from server',
               235: '235 Auth failed',
               354: 'Error with data'
               }
    if ans[:3] != str(code):
        raise Exception(answers[code])


def b(s):
    return bytes(s, encoding="utf-8")


def send_and_get_answer(sock, msg):
    sock.send((msg.decode() + "\n").encode())
    ans = sock.recv(1024).decode()
    print(ans)
    return ans


if __name__ == '__main__':
    main()
