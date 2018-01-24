# TODO: Comment this file XD

import socket
import threading
import sys

command = None

HOST = 'localhost'    # The remote host
PORT = 8000              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receiveData():
    while True:
        try:
            d = s.recv(1024)
            print(d.decode())
        except:
            print("Error: server disconected")
            break


receiveThread = threading.Thread(
    None, receiveData, 'receive_thread')


def main():
    global HOST

    print('PyChat by Elite Fun - 2018')
    print('write \'STOP\' to exit client')
    name = input('Please enter your name: ')
    if (len(sys.argv) > 1):
        # user gave custom host
        HOST = sys.argv[1]

    s.connect((HOST, PORT))

    name_message = '$(NAME) ' + name

    s.send(str.encode(name_message))

    receiveThread.start()

    while True:
        command = input()
        if command == 'STOP':
            break
        s.send(str.encode(command))

    s.close()


if __name__ == '__main__':
    main()
