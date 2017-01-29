# coding:utf-8
import socket
ip = ''
port = 8017
def socket_send(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    if command[:4] == 'cmd ':
        sock.send(command)
        result = sock.recv(2048)
        sock.close()
        print result
        return
    else:
        sock.send(command)
        sock.close()
while True:
    cmd = raw_input('cmd:')
    socket_send(cmd)
