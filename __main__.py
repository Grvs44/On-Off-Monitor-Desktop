from OnOffMonitor import *
from time import sleep
def DownloadLog():
    validate = ValidateNumber(lognumdl.get())
    if validate:
        f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")],parent=window)
        if f != None:
            try:
                print(lognumdl.get())
                f.write(GetData(DeviceIPAddress(devsel.get()),"/log.csv",postlist=[["lognum",lognumdl.get()],["fileage",fileagedl.get()]]).split("\r\n\r\n")[1])
                f.close()
                showinfo("Download log file","Log file downloaded to " + f.name)
            except ConnectionRefusedError: ConnectionRefused(devsel.get(),window)
    else:
        showerror("Download log file","The number of log files must be a positive integer",parent=window)
def DeleteLog():
    validate = ValidateNumber(lognumd.get())
    if validate:
        if askyesno("Delete log files","Are you sure you want to delete the chosen log files?"):
            try: showinfo("Delete log files",GetData(DeviceIPAddress(devsel.get()),"/deletelogs",postlist=[["lognum",lognumd.get()],["fileage",fileaged.get()],["app","1"]]).split("\r\n\r\n")[1])
            except ConnectionRefusedError: ConnectionRefused(devsel.get(),window)
    else:
        showerror("Delete log filed","The number of log files must be a positive integer",parent=window)
def ShutDown():
    if askyesno("Shut down","Are you sure you want to shut down?"):
        try: showinfo("Shut down",GetData(DeviceIPAddress(devsel.get()),"/shutdown",postlist=[["devices",sddevice.get()],["web",sdweb.get()],["app","1"]]).split("\r\n\r\n")[1])
        except ConnectionRefusedError: ConnectionRefused(devsel.get(),window)
def AddMenubarCommands(menu,commands):
    for command in commands:
        if len(command) == 2: menu.add_command(label=command[0],command=command[1])
        else: menu.add_separator()
def Settings():
    page = Toplevel()
    page.title("On/Off Monitor Settings")
    page.grid_rowconfigure(1,weight=0)
    page.grid_rowconfigure(2,weight=0)
    page.grid_rowconfigure(3,weight=1)
    page.grid_rowconfigure(4,weight=0)
    page.grid_rowconfigure(5,weight=0)
    page.grid_columnconfigure(1,weight=1)
    page.grid_columnconfigure(2,weight=1)
    page.grid_columnconfigure(3,weight=1)
    page.grid_columnconfigure(4,weight=0)
    Label(page,text="Settings",font=fonts.h1).grid(row=1,column=1,columnspan=3,sticky="NSEW")
    Label(page,text="Devices",font=fonts.h2).grid(row=2,column=1,columnspan=3,sticky="NSEW")
    devicelist = Listbox(page,font=fonts.p,selectmode="multiple")
    scroll_v = Scrollbar(page,command=devicelist.yview)
    scroll_h = Scrollbar(page,command=devicelist.xview,orient="horizontal")
    devicelist.config(xscrollcommand=scroll_h.set,yscrollcommand=scroll_v.set)
    scroll_v.grid(row=3,column=4,sticky="NSEW")
    scroll_h.grid(row=4,column=1,columnspan=3,sticky="NSEW")
    devicelist.grid(row=3,column=1,columnspan=3,sticky="NSEW")
    Button(page,text="Add new",font=fonts.p,command=lambda:AddDevice(devicelist)).grid(row=5,column=1)
    Button(page,text="Remove selected",font=fonts.p,command=lambda:RemoveDevice(devicelist,page)).grid(row=5,column=3)
    Button(page,text="Set as default device",font=fonts.p,command=lambda:SetDefaultDevice(devicelist,page)).grid(row=5,column=2)
    for i in range(len(settings["devices"])): devicelist.insert(i,FormatDeviceName(i))
    page.mainloop()
def AddDevice(listbox):
    newname = askstring("Add device","Please enter the name of the new device")
    if newname != None and newname != "":
        newip = askstring("Add device","Please enter the IP address with port number (if required) of "+newname)
        if ValidateIPAddress(newip):
            settings["devices"].append([newname,newip])
            listbox.insert(len(settings["devices"]),newname+" ("+newip+")")
            SaveSettings()
            devicemenu["menu"].add_command(label=newname+" ("+newip+")")
def RemoveDevice(listbox,window):
    index=listbox.curselection()
    if len(index)>0:
        if askyesno("Remove device","Are you sure you want to delete the selected devices?",parent=window):
            deleted = "Removed device(s):"
            for i in range(len(index)-1,-1,-1):
                delitem=settings["devices"].pop(index[i])
                deleted += "\n" + delitem[0] + " (" + delitem[1] + ")"
                listbox.delete(index[i])
                devicemenu["menu"].delete(index[i])
            if settings["defaultip"] in index:
                CheckDefaultDevice(updated=True)
                deleted+="\nSet "+FormatDeviceName(0)+" as the default device"
            SaveSettings()
            showinfo("Remove device",deleted,parent=window)
def LogFileList():
    device = devsel.get()
    page = Toplevel()
    page.title(device + " log files - On/Off Monitor")
    page.grid_rowconfigure(1,weight=0)
    page.grid_rowconfigure(2,weight=1)
    page.grid_rowconfigure(3,weight=0)
    page.grid_rowconfigure(4,weight=0)
    page.grid_columnconfigure(1,weight=1)
    page.grid_columnconfigure(2,weight=1)
    page.grid_columnconfigure(3,weight=1)
    page.grid_columnconfigure(4,weight=0)
    Label(page,text=device + " log files",font=fonts.h1).grid(row=1,column=1,columnspan=4,sticky="NSEW")
    devicelist = Listbox(page,font=fonts.p,selectmode="multiple")
    scroll_v = Scrollbar(page,command=devicelist.yview)
    scroll_h = Scrollbar(page,command=devicelist.xview,orient="horizontal")
    devicelist.config(xscrollcommand=scroll_h.set,yscrollcommand=scroll_v.set)
    scroll_v.grid(row=2,column=4,sticky="NSEW")
    scroll_h.grid(row=3,column=1,columnspan=3,sticky="NSEW")
    devicelist.grid(row=2,column=1,columnspan=3,sticky="NSEW")
    Button(page,text="Refresh",font=fonts.p,command=lambda:RefreshLogFileList(device,devicelist,page)).grid(row=4,column=1)
    Button(page,text="Delete",font=fonts.p,command=lambda:DeleteLogFile(device,devicelist,page)).grid(row=4,column=2)
    Button(page,text="Open",font=fonts.p,command=lambda:OpenLogFile(device,devicelist,page)).grid(row=4,column=3)
    RefreshLogFileList(device,devicelist,page)
    if devicelist.size() == 0: page.destroy()
    page.mainloop()
def RefreshLogFileList(device,listbox,window):
    try:
        data = GetData(DeviceIPAddress(device),"/logfilelist",postlist=[["app","1"]])
        data = loads(GetBody(data))
        listbox.delete(0,"end")
        for i in range(len(data)): listbox.insert(i,data[i][:4] + "/" + data[i][4:6] + "/" + data[i][6:8])
    except ConnectionRefusedError: ConnectionRefused(device,window)
def DeleteLogFile(device,listbox,window):
    if len(listbox.curselection())>0:
        if askyesno("Delete log files","Are you sure you want to delete the selected items?",parent=window):  
            response=""
            index=list(listbox.curselection())
            print(index)
            for i in range(len(index)-1,-1,-1):
                try:
                    response+=GetBody(GetData(DeviceIPAddress(device),"/deletelocallog",postlist=[["app","1"],["lognum",str(index[i])]]))+"\n"
                    listbox.delete(index[i])
                except ConnectionRefusedError: ConnectionRefused(device,window)
            showinfo("Delete log files",response,parent=window)
def OpenLogFile(device,listbox,window):
    selection = listbox.curselection()
    if len(selection)>0:
        f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")])
        if f != None:
            try:
                data=[]
                for index in selection: data.extend(loads(GetBody(GetData(DeviceIPAddress(device),"/logfile",[["lognum",str(index)],["app","1"]]))))
                f.write(ListToCsv("Date,Time,Device,Status",data))
                showinfo("Open log file","Log file saved to "+f.name)
            except ConnectionRefusedError: ConnectionRefused(device,window)
            f.close()
def SetDefaultDevice(listbox,window):
    index=listbox.curselection()
    if len(index)>0:
        index=index[0]
        settings["defaultip"]=index
        devsel.set(FormatDeviceName(index))
        SaveSettings()
        showinfo("On/Off Monitor Settings",FormatDeviceName(index) + " was set as the default device",parent=window)
def CheckDefaultDevice(updated=False):
    if updated or settings["defaultip"] not in range(len(settings["devices"])):
        if len(settings["devices"]) == 0:
            settings["defaultip"] = None
            devsel.set("(No devices)")
            showinfo("On/Off Monitor","No devices have been set up. Please go to Options > Settings and set up at least one On/Off Monitor device.")
        else:
            settings["defaultip"] = 0
            devsel.set(FormatDeviceName(0))
def UpdateDeleteText(e):
    delrad1.config(text="Delete "+lognumd.get()+" of the oldest files")
    delrad2.config(text="Keep "+lognumd.get()+" of the newest files")
def ConnectionRefused(device,window): showerror("On/Off Monitor",device + " could not be reached. Please check that it is running On/Off Monitor and connected to the same network.",parent=window)

# LiveStatus
def Status(devsel):
    ipaddress = DeviceIPAddress(devsel.get())
    if not ValidateIPAddress(ipaddress):
        showerror("Live Device Status - On/Off Monitor","Invalid IP Address")
        return
    from threading import Thread
    win = Tk()
    win.title("Live Device Status - On/Off Monitor")
    win.grid_columnconfigure(1,weight=1)
    win.grid_columnconfigure(2,weight=1)
    win.grid_rowconfigure(4,weight=1)
    table = [Listbox(win,font=fonts.p,selectmode="none",justify="center"),Listbox(win,font=fonts.p,selectmode="none",justify="center")]
    refresh = Entry(win)
    Label(win,text="Live Device Status",font=fonts.h1).grid(row=1,column=1,columnspan=3,sticky="NSEW")
    Label(win,text="Refresh frequency (sec)",font=fonts.p).grid(row=2,column=1,sticky="NSE")
    refresh.grid(row=2,column=2,sticky="NSW")
    Label(win,text="Name",font=fonts.h2).grid(row=3,column=1,sticky="NSEW")
    Label(win,text="Status",font=fonts.h2).grid(row=3,column=2,sticky="NSEW")
    table[0].grid(row=4,column=1,sticky="NSEW")
    table[1].grid(row=4,column=2,sticky="NSEW")
    Thread(target=RequestStatus,args=(win,table,refresh,ipaddress,devsel)).start()
    win.mainloop()
def RequestStatus(win,table,refresh,ipaddress,devsel):
    try:
        while True:
            table[0].delete(0,END)
            table[1].delete(0,END)
            data = loads(GetBody(GetData(ipaddress,"/status/status.json")))
            for i in range(len(data)):
                for j in [0,1]:
                    table[j].insert(i,data[i][j])
            sleep(sleeptime(refresh))
    except TclError: pass # When win closes and window is still open
    except RuntimeError: pass # When win closes and window is already closed
    except ConnectionRefusedError:
        ConnectionRefused(devsel.get(),win)
        win.destroy()
def sleeptime(refresh):
    try:
        number = float(refresh.get())
        if number < 0.05: return 10
        else: return number
    except ValueError: return 10

window = Tk()
window.title("On/Off Monitor")
print(window.wm_iconwindow())
menubar = Menu(window,font=fonts.p)
window.config(menu = menubar)
optionsmenu = Menu(menubar, tearoff = 0)
AddMenubarCommands(optionsmenu,[("Settings",Settings),(),("Exit",window.destroy)])
menubar.add_cascade(label="Options", menu=optionsmenu)

window.grid_columnconfigure(1,weight=1)
window.grid_columnconfigure(2,weight=1)
window.grid_columnconfigure(3,weight=1)

fileagedl = StringVar() #Fileage for download logs
fileaged = StringVar() #Fileage for delete logs
sddevice = StringVar() #Shut down this or all devices
sdweb = StringVar() #Shut down web or devices
devsel = StringVar() #Variable to chose device to send/receive requests
fileagedl.set("new")
fileaged.set("old")
sddevice.set("this")
sdweb.set("web")
if settings["defaultip"] != None: devsel.set(FormatDeviceName(settings["defaultip"]))
Label(window,text="On/Off Monitor",font=fonts.h1).grid(row=1,column=1,columnspan=3)
Label(window,text="Devices",font=fonts.h2).grid(row=2,column=3,rowspan=2)
devicemenu = OptionMenu(window,devsel,*settings["devices"])
devicemenu.grid(row=4,column=3)
Button(window,text="Log file list",command=LogFileList,font=fonts.p).grid(row=5,column=3)

Label(window,text="Log files",font=fonts.h2).grid(row=2,column=1)
Label(window,text="Download",font=fonts.h3).grid(row=3,column=1)
lognumdl = Entry(window,font=fonts.p)
lognumdl.grid(row=4,column=1)
Radiobutton(window,text="of the oldest files",variable=fileagedl,value="old",font=fonts.p).grid(row=5,column=1)
Radiobutton(window,text="of the newest files",variable=fileagedl,value="new",font=fonts.p).grid(row=6,column=1)
Button(window,text="Download",command=DownloadLog,font=fonts.p).grid(row=7,column=1)

Label(window,text="Delete",font=fonts.h3).grid(row=8,column=1)
lognumd = Entry(window,font=fonts.p)
lognumd.grid(row=9,column=1)
delrad1 = Radiobutton(window,text="Delete ^ of the oldest files",variable=fileaged,value="old",font=fonts.p)
delrad1.grid(row=10,column=1)
delrad2 = Radiobutton(window,text="Keep ^ of the newest files",variable=fileaged,value="new",font=fonts.p)
delrad2.grid(row=11,column=1)
Button(window,text="Delete",command=DeleteLog,font=fonts.p).grid(row=12,column=1)
lognumd.bind("<KeyRelease>",UpdateDeleteText)

Label(window,text="Shutdown",font=fonts.h2).grid(row=2,column=2,rowspan=2)
Radiobutton(window,text="This device",variable=sddevice,value="this",font=fonts.p).grid(row=4,column=2)
Radiobutton(window,text="All devices",variable=sddevice,value="all",font=fonts.p).grid(row=5,column=2)
Radiobutton(window,text="On/Off Monitor",variable=sdweb,value="web",font=fonts.p).grid(row=6,column=2)
Radiobutton(window,text="On/Off Monitor and device",variable=sdweb,value="all",font=fonts.p).grid(row=7,column=2)
Button(window,text="Shut down",command=ShutDown,font=fonts.p).grid(row=8,column=2)

Button(window,text="Live Device Status",font=fonts.p,command=lambda:Status(devsel)).grid(row=8,column=3)
CheckDefaultDevice()
window.mainloop()
