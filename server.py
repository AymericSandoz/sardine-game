import socket
from _thread import *
import pickle
import json
from entities import player_instances, MAX_PLAYERS
server = '192.168.43.18'  # Assurez-vous que cette adresse est correcte
# server = ''
port = 5555
import sys
print(sys.version)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print(f"Server bound to {server}:{port}")
except socket.error as e:
    print(f"Socket error: {e}")

s.listen(MAX_PLAYERS)
print(f"Server listening, ready for up to {MAX_PLAYERS} players")

players = player_instances
print(f"Initial player list: {players}")


def threaded_client(conn, player):
    try:
        print("v1")
        print(f"Sending player {player} to client :", players[player])
        print(f"Sending player {player} to client :",
              pickle.dumps(players[player]))
        conn.send(pickle.dumps(players[player]))
        while True:
            print(f"true")
            print("Waiting for data...")
            raw_data = conn.recv(2048)
            print("Data received. Deserializing...", raw_data)
            print("pickle.loads(raw_data) :", pickle.loads(raw_data))
            data = pickle.loads(raw_data)
            print("Data deserialized.")
            print(f"Received data from player {player}: {data}")
            if not data:
                break
            players[player] = data
            reply = players[:player] + players[player+1:]
            print("pickle.dumps(reply) :", pickle.dumps(reply))
            conn.sendall(pickle.dumps(reply))
    except Exception as e:
        print(f"Error handling client {player}: {e}")
    finally:
        print(f"Connection with player {player} closed")
        conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}, connection object: {conn}")
    if currentPlayer < MAX_PLAYERS:
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1
        print(f"Current player count: {currentPlayer}")
    else:
        print("Server full: already reached maximum player count.")
