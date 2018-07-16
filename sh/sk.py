#-*-coding:utf-8-*-

import threading
import socket
import dao

class Sv:
    def __init__(self):
        self.host = ''
        self.dao = dao.DAO()
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.cnt = 0


    def listen(self):
        self.sock.listen(999999)
        while True:
            client, address = self.sock.accept()
            self.cnt += 1
            #print("Accept ", self.cnt)
            threading.Thread(target = self.listenToClient, args = (client,address,self.cnt)).start()


    def listenToClient(self, client, address, cnt):
        size = 1024
        while True:
            try:
                #print('Waiting...{}'.format(cnt))
                data = client.recv(size)
                if data != 0:
                    rp = data.decode("utf-8")
                    #print("rp : {} rptype : {}".format(rp,type(rp)))
                    rps = rp.split("::")
                    #print(rps[0],"   ",rps[1])
                    self.dao.insert_data(rps[0],rps[1])
                    #print("response : ",rp)
                    #client.send(response)
                #else:
                    
                    #print('Client disconnected')

            except:
                '''  except '''
                #print("except")
                #client.close()
                #return False



if __name__=="__main__":
    sv = Sv()
    sv.listen()
    
