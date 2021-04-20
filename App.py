from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR
import pickle,json
try: from tkinter import *
except ModuleNotFoundError: from Tkinter import *
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
def DownloadLog():
    print("DL")
window = Tk()
window.title("On/Off Monitor")
window.resizable(0,0)
fileagedl = StringVar() #Fileage for download logs
fileaged = StringVar() #Fileage for delete logs
Label(window,text="Log files").grid(row=1,column=1)
Label(window,text="Download").grid(row=2,column=1)
lognumdl = Entry(window)
lognumdl.grid(row=3,column=1)
Radiobutton(window,text="of the oldest files",variable=fileagedl,value="old").grid(row=4,column=1)
Radiobutton(window,text="of the newest files",variable=fileagedl,value="new").grid(row=5,column=1)
Button(window,text="Download",command=DownloadLog).grid(row=6,column=1)
Label(window,text="Delete").grid(row=7,column=1)
lognumd = Entry(window)
lognumd.grid(row=8,column=1)
window.mainloop()
