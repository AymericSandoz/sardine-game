import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "172.233.245.56"
        self.server = "192.168.43.18"  # local
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Connected to server at {self.addr}")
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(f"Connection error: {e}")

    def send(self, data):
        try:
            print("data", pickle.dumps(data))
            bytes_sent = self.client.send(pickle.dumps(data))
            print(f"Bytes sent: {bytes_sent}")
            recv = self.client.recv(2048)
            print("recv", recv)
            return pickle.loads(recv)
        except socket.error as e:
            print(f"Socket error: {e}, bytes sent: {bytes_sent}")
        except EOFError as e:
            print(
                f"EOF error: {e}. The connection may have been lost. bytes sent: {bytes_sent}")
        except Exception as e:
            print(f"General error: {e}")
