import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
print("-----------------------------MULTI KLIEN CHAT SERVER-------------------------------------------\n-----------------------------MASUKKAN KREDENSIAL UNTUK MENGHUBUNGKAN KE SERVER--------------------------")


ip = input('                    MASUKKAN IP ADDRESS YANG INGIN DISAMBUNGKAN\n                    IP ADDRESS:')
uname = input(
    "                    MASUKKAN USERNAME UNTUK DITAMPILKAN SAAT CHATTING\n                    USERNAME:")
try:
    s.connect((ip, port))
except:
    print("\n\t GAGAL TERSAMBUNG....PASTIKAN MEMASUKKAN IP ADDRESS YANG BENAR\n")
try:
    s.send(uname.encode('ascii'))

    clientRunning = True

    def receiveMsg(sock):
        serverDown = False
        while clientRunning and (not serverDown):
            try:
                msg = sock.recv(1024).decode('ascii')
                print(msg)
            except:
                print(
                    'SERVER BERHENTI....SILAHKAN TEKAN TOMBOL APAPUN UNTUK KELUAR.......')
                serverDown = True

    threading.Thread(target=receiveMsg, args=(s,)).start()
    while clientRunning:
        tempMsg = input()

        if tempMsg.startswith('@') and ' ' in tempMsg:
            recipients, message = tempMsg.split(' ', 1)
            recipients = recipients.replace('@', '').strip()
            msg = '@' + recipients + ' ' + message
        else:
            msg = uname + ' :::>>> ' + tempMsg

        if '#exitapp' in msg:
            clientRunning = False
            s.send('#exitapp'.encode('ascii'))
        else:
            s.send(msg.encode('ascii'))

except:
    print("\n\t OOPS ERROR\n")
