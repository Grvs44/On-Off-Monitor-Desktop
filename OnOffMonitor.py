from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR
from json import loads,load,dump
def GetData(address,path,postlist=[]):
    method = "GET"
    if len(postlist)>0: method = "POST"
    post = ""
    for i in range(len(postlist)):
        post+=str(postlist[i][0])+"="+str(postlist[i][1])
        if i+1 != len(postlist): post+="&"
    addressparts = address.split(":")
    if len(addressparts) == 1: addressparts.append(80)
    clientsocket = socket(AF_INET,SOCK_STREAM)
    clientsocket.connect((addressparts[0], int(addressparts[1])))
    cmd = (method+' '+path+' HTTP/1.1\r\n\r\n'+post).encode()
    clientsocket.send(cmd)
    data = "".encode()
    while True:
        data += clientsocket.recv(512)
        if len(newdata) < 1: break
    clientsocket.close()
    return data.decode()
def ListToCsv(header,item):
    csv=header+"\n"
    for i in range(len(item)):
        for j in range(len(item[i])):
            csv+=str(item[i][j])
            if j+1 != len(item[i]): csv+=","
        if i+1 != len(item): csv+="\n"
    return csv
class Settings():
    devices=["192.168.0.169"]
def GetSettings(path="settings.json"):
    f=open(path,"r")
    read = load(f)
    print(f)
    print(read)
    f.close()
def SaveSettings(path="settings.json"):
    f=open(path,"w")
    dump(["192.168.0.169"],f)
    f.close()
