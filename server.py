import socket
import configparser
from collections import defaultdict
import re
from http import HTTPStatus

config = configparser.RawConfigParser()
config.read('config.ini')
address = (config.get('host', 'ip'), int(config.get('host', 'port')))

my_socket = socket.socket(family=socket.AF_INET,
                          type=socket.SOCK_STREAM,
                          proto=0,
                          fileno=None)
my_socket.bind(address)
my_socket.listen(10)
print('=======Server started=======')
conn, addr = my_socket.accept()
print(conn, addr)


def message_parser(message):
    response = defaultdict(
        lambda: {"Request Method": "GET", "Request Source": None, "Response Status": "200 OK", "header-name": None}
    )
    method = re.search(r'(POST|GET|PUT|DELETE|HEAD)', message)

    if method is not None:
        response["Request Method"] = method.groups()[0]
    else:
        response["Request Method"] = 'GET'

    response["Request Source"] = addr
    status = re.search(r'status=(\d{3})', message)

    if status is not None:
        for item in list(HTTPStatus):
            if item.value == int(status.groups()[0]):
                response["Response Status"] = f'{item.value} {item.phrase}'
                break
            else:
                response["Response Status"] = '200 OK'
    else:
        response["Response Status"] = '200 OK'

    list_headers = re.findall(r'\S+: \S+', message)

    if list_headers is not None:
        response = ' '.join([f'{key}: {value}' for key, value in response.items()] + list_headers)

    return response


while True:
    data = conn.recv(1024)
    resp = message_parser(data.decode('UTF-8'))
    if data == b'stop':
        break
    print(resp)

my_socket.close()
