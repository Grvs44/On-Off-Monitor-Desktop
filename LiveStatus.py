from OnOffMonitor import *
from time import sleep
def Status(parent=None):
    from threading import Thread
    win = Tk()
    win.title("Live Device Status - On/Off Monitor")
    win.grid_columnconfigure(1,weight=1)
    win.grid_columnconfigure(2,weight=1)
    win.grid_rowconfigure(4,weight=1)
    table = [Listbox(win,font=fonts.p,selectmode="none",justify="center"),Listbox(win,font=fonts.p,selectmode="none",justify="center")]
    #scroll = Scrollbar(win,command=(table[0].yview,table[1].yview))
    #table[0].config(yscrollcommand=scroll.set)
    #table[1].config(yscrollcommand=scroll.set)
    refresh = Entry(win)
    Label(win,text="Live Device Status",font=fonts.h1).grid(row=1,column=1,columnspan=3,sticky="NSEW")
    Label(win,text="Refresh frequency (sec)",font=fonts.p).grid(row=2,column=1,sticky="NSE")
    refresh.grid(row=2,column=2,sticky="NSW")
    Label(win,text="Name",font=fonts.h2).grid(row=3,column=1,sticky="NSEW")
    Label(win,text="Status",font=fonts.h2).grid(row=3,column=2,sticky="NSEW")
    table[0].grid(row=4,column=1,sticky="NSEW")
    table[1].grid(row=4,column=2,sticky="NSEW")
    #scroll.grid(row=3,column=3,rowspan=2,sticky="NSEW")
    Thread(target=RequestStatus,args=(win,table,refresh)).start()
    win.mainloop()
def RequestStatus(win,table,refresh):
    try:
        while True:
            table[0].delete(0,END)
            table[1].delete(0,END)
            data = loads(GetData("192.168.0.139","/status/status.json").split("\r\n\r\n")[1])
            for i in range(len(data)):
                for j in [0,1]:
                    table[j].insert(i,data[i][j])
            sleep(sleeptime(refresh))
    except TclError: pass #When win closes and window is still open
    except RuntimeError: pass #When win closes and window is already closed
def sleeptime(refresh):
    try:
        number = float(refresh.get())
        if number < 0.05: return 10
        else: return number
    except ValueError: return 10
