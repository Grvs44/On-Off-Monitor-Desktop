from OnOffMonitor import *
from time import sleep
def Status(parent=None):
    from threading import Thread
    win = Tk()
    win.title("Live Device Status - On/Off Monitor")
    win.grid_columnconfigure(1,weight=1)
    win.grid_columnconfigure(2,weight=1)
    table = Frame(win)
    refresh = Entry(win)
    Label(win,text="Live Device Status",font=fonts.h1).grid(row=1,column=1,columnspan=2,sticky="NSEW")
    Label(win,text="Refresh frequency (sec)",font=fonts.p).grid(row=2,column=1,sticky="NSEW")
    refresh.grid(row=2,column=2,sticky="NSEW")
    Label(win,text="Name",font=fonts.h2).grid(row=3,column=1,sticky="NSEW")
    Label(win,text="Status",font=fonts.h2).grid(row=3,column=2,sticky="NSEW")
    Thread(target=RequestStatus,args=(win,table,refresh)).start()
    win.mainloop()
def RequestStatus(win,table,refresh):
    try:
        while True:
            for widget in table.winfo_children(): widget.destroy()
            data = loads(GetData("192.168.0.139","/status/status.json").split("\r\n\r\n")[1])
            for i in range(len(data)):
                for j in range(len(data[i])):
                    Label(win,text=data[i][j],font=fonts.p).grid(row=i+4,column=j+1)
            sleep(sleeptime(refresh))
    except TclError: print("TclError")
    except RuntimeError: print("RuntimeError")
def sleeptime(refresh):
    try:
        number = float(refresh.get())
        if number < 0.05: return 10
        else: return number
    except ValueError: return 10
