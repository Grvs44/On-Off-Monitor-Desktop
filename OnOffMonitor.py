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
        newdata = clientsocket.recv(512)
        if len(newdata) < 1: break
        data += newdata
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
def GetSettings(path="settings.json"):
    try:
        f=open(path,"r")
        read = load(f)
        f.close()
        return read
    except FileNotFoundError: return {"defaultip":None,"devices":[]}
def SaveSettings(path="settings.json"):
    f=open(path,"w")
    dump(settings,f)
    f.close()
class fonts():
    h1=("Segoe UI",24)
    h2=("Segoe UI",16)
    h3=("Segoe UI",13)
    p=("Segoe UI",10)
def ValidateNumber(value):
    if "." in value: return False
    else:
        try:
            value = int(value)
            if value < 1: return False
            else: return True
        except ValueError: return False
def ValidateIPAddress(value):
    return value != None and value != "" and "." in value
def FormatDeviceName(index): return settings["devices"][index][0]+" ("+settings["devices"][index][1]+")"
def DeviceIPAddress(device): return device.split("(")[1].split(")")[0]
def ConnectionRefused(device): showerror("On/Off Monitor",device + " could not be reached. Please check that it is running On/Off Monitor and connected to the same network.")
def GetBody(response): return response.split("\r\n\r\n")[1]
settings=GetSettings()
