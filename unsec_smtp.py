import socket

HOST = "smtp.yandex.ru"
PORT = 587


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Connecting to {HOST}, port: {PORT}")
    s.connect((HOST, PORT))
    connect_answer = s.recv(65536)
    print(connect_answer.decode())
    msg = "EHLO x\n"
    print(f"Sending helo message: {msg}")
    s.send(msg.encode())
    helo_answer = s.recv(1024)
    print(helo_answer.decode())
    auth = "AUTH LOGIN\n"
    print(f"Trying to authorization with {auth}")
    s.send(auth.encode())
    auth_answer = s.recv(1024)
    print(auth_answer.decode())


if __name__ == '__main__':
    main()
