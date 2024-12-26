import socket
import os
import sys

server = "irc.chat.twitch.tv"
port = 6667
nickname = os.environ.get('TWITCH_NICKNAME')
token = os.environ.get('TWITCH_TOKEN')

if len(sys.argv) != 2:
    print("Usage: python main.py <channel>")
    sys.exit(1)

channel = "#" + sys.argv[1]

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

active_users = set()

try:
    while True:
        response = sock.recv(2048).decode('utf-8')
        
        if response.startswith('PING'):
            sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
        
        elif "PRIVMSG" in response:
            user = response.split('')[0][1:]
            active_users.add(user)
            print(f"Message from: {user}")
            print(f"Active users: {len(active_users)}")
except KeyboardInterrupt:
    print("Disconnecting...")
finally:
    sock.close()
