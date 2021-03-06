import socket
import threading

# max number of bytes to be received from clients
RECV_BUF_SIZE = 1024

HOST = ''
PORT = 8000


class Client:
    def __init__(self, conn, addr):
        self.connection = conn
        self.address = addr
        self.name = addr[0]

    def setName(self, name):
        self.name = name

    def receiveData(self):
        data = self.connection.recv(RECV_BUF_SIZE)
        if data:
            return(data.decode())
        else:
            return False

    def sendData(self, data, name):
        try:
            message = '(' + name + ') ' + data
            self.connection.send(str.encode(message))
        except:
            return False

    def closeConn(self):
        self.connection.close()


# modified from : https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client

class ThreadedServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        self.sock.bind((self.host, self.port))  # bind it to given host & port
        self.clients = []  # list of clients

    def listen(self):
        self.sock.listen()
        while True:
            client, address = self.sock.accept()  # accept any new client
            print('New connection:', address)
            threading.Thread(target=self.listenToClient,
                             args=(client, address)).start()

    def listenToClient(self, client, address):
        c = Client(client, address)
        self.clients.append(c)  # add client to list of clients

        while True:
            try:
                data = c.receiveData()  # receive data from clients
                if data:
                    if (data.startswith('$(NAME)')):
                        c.setName(data[8:])
                        print('changed client name')
                    else:
                        self.sendToClients(data, c.name)
                        print(data)
                else:
                    raise ('Client {} disconnected'.format(address))
                    self.clients.remove(c)
            except:
                c.closeConn()
                print('Client {} disconnected'.format(c.name))
                self.clients.remove(c)
                return False

    def sendToClients(self, m, n):
        for c in self.clients:
            try:
                c.sendData(m, n)
            except:
                print("error while sending data to client. Maybe he disconnected?")
                self.clients.remove(c)
                # need to remove the client from the list


def main():
    ThreadedServer(HOST, PORT).listen()  # start the server


if __name__ == "__main__":
    main()
