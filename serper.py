import socket
import threading
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRunning = True
ip = str(socket.gethostbyname(socket.gethostname()))
port = 1234

clients = {}

# s.bind(('127.0.0.1', port)) #localhost
s.bind((ip, port))
s.listen()
print('SERVER DIMULAI\nDENGAN IP ADDRESS:%s\n' % ip)

localtime = time.asctime(time.localtime(time.time()))
print("SERVER DIMULAI PADA::", localtime)


def handleClient(client, uname):
    clientConnected = True
    keys = clients.keys()
    help = 'CARA MENGGNAKANNYA:\n Broadcast: #toall pesan \n Mengirim ke satu user: @username, pesan \n Mengirim multi user: @username1, username2 pesan\n Melihat user yang terhubung: #showconnectedusers\n Untuk keluar chat: #exitapp'

    while clientConnected:
        try:
            msg = client.recv(1024).decode('ascii')
            response = 'PENGGUNA YANG TERHUIBUNG:\n'
            found = False
            if '#showconnectedusers' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) + '\t:' + name+'\n'
                client.send(response.encode('ascii'))
            elif '#showmanual' in msg:
                client.send(help.encode('ascii'))
            elif '#toall' in msg:
                msg = msg.replace('#toall', '')
                for k, v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '#exitapp' in msg:
                response = 'KONEKSI KLIEN TERPUTUS'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                localtime = time.asctime(time.localtime(time.time()))

                print(uname + ' MENINGGALKAN PESAN PADA %s' % localtime)
                print(
                    '\n------------------------------------------------------------------------------------------------------\n')
                clientConnected = False
            else:
                if ',' in msg and msg[0] == '@':
                    recipients, message = msg.split(' ', 1)
                    recipients = recipients.replace('@', '').strip().split(',')
                    for recipient in recipients:
                        if recipient in keys and recipient != uname:
                            clients[recipient].send(
                                (uname + ': ' + message).encode('ascii'))
                            found = True
                    if not found:
                        client.send(
                            'USERNAME TIDAK VALID, SILAHKAN DIULANG LAGI'.encode('ascii'))
                else:
                    client.send(
                        'COMMAND ATAU USERNAME TIDAK VALID'.encode('ascii'))
        except:
            clients.pop(uname)
            localtime = time.asctime(time.localtime(time.time()))
            print(uname + ' MENINGGALKAN PESAN PADA %s' % localtime)
            print('\n------------------------------------------------------------------------------------------------------\n')
            clientConnected = False


while serverRunning:
    client, address = s.accept()
    uname = client.recv(1024).decode('ascii')
    localtime = time.asctime(time.localtime(time.time()))
    print('--------------%s TERHUBUNG KE SERVER' % str(uname))
    print('PADA WAKTU %s' % localtime)
    print('--------------')
    client.send(
        'KAMU TELAH TERHUBUNG KE SERVER CHAT\nUNTUK MELIHAT MANUAL SIALHKAN MENGIRIM #showmanual'.encode('ascii'))

    if (client not in clients):
        clients[uname] = client
        threading.Thread(target=handleClient, args=(client, uname, )).start()
