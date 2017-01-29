# coding:utf-8
import socket, os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myname = socket.getfqdn(socket.gethostname())
ip = socket.gethostbyname(myname)
port = 8017
sock.bind((ip, port))
sock.listen(5)
from ctypes import windll

WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_UP = 0x0a
APPCOMMAND_VOLUME_DOWN = 0x09
APPCOMMAND_VOLUME_MUTE = 0x08

def mute():
    hwnd = windll.user32.GetForegroundWindow()
    windll.user32.PostMessageA(hwnd, WM_APPCOMMAND
                               , 0, APPCOMMAND_VOLUME_MUTE * 0x10000)


def upv():
    hwnd = windll.user32.GetForegroundWindow()
    windll.user32.PostMessageA(hwnd, WM_APPCOMMAND
                               , 0x30292, APPCOMMAND_VOLUME_UP * 0x10000)


def downv():
    hwnd = windll.user32.GetForegroundWindow()
    windll.user32.PostMessageA(hwnd, WM_APPCOMMAND
                               , 0x30292, APPCOMMAND_VOLUME_DOWN * 0x10000)


count = 0
while True:
    connection, address = sock.accept()
    try:
        connection.settimeout(5)
        buf = connection.recv(1024)
        if buf == '1' or buf == '0':
            mute()
            count += 1
        elif buf == '+':
            upv()
            count += 1
        elif buf == '-':
            downv()
            count += 1
        elif buf == '-1':
            result = os.popen('shutdown -s -t 1').read()
        elif buf[:4] == 'cmd ':
            result = os.popen(buf[4:]).read()
            connection.send(result)
    except socket.timeout:
        connection.close()
