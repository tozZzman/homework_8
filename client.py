import socket
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')
address = (config.get('host', 'ip'), int(config.get('host', 'port')))

my_socket = socket.socket()
conn = my_socket.connect(address)

while True:
    message = str(input('Enter query: ').replace('\r', ' ').replace('\n', ' '))
    msg_bytes = my_socket.send(bytes(message, encoding='UTF-8'))
    if message == 'stop':
        break
    print(f'Send {msg_bytes} bytes')

my_socket.close()
