from OnOffMonitor import *
try:
    from tkinter import Tk,StringVar,Label,Entry,Button,Radiobutton,Menu,Toplevel,Listbox,OptionMenu
    from tkinter.filedialog import asksaveasfile
    from tkinter.messagebox import showinfo,askyesno,showerror
    from tkinter.simpledialog import askstring
except ImportError:
    from Tkinter import *
    from tkFileDialog import asksaveasfile
    from tkMessageBox import showinfo,askyesno,showerror
    from tkSimpleDialog import askstring
def DownloadLog():
    validate = ValidateNumber(fileagedl.get())
    if validate:
        f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")])
        if f != None:
            try:
                f.write(GetData(GetCurrentDeviceIP(),"/log.csv",postlist=[["lognum",lognumdl.get()],["fileage",fileagedl.get()]]).split("\r\n\r\n")[1])
                f.close()
                showinfo("Download log file","Log file downloaded to " + f.name)
            except ConnectionRefusedError: showerror("Download log file",devsel.get() + " could not be reached")
    else:
        showerror("Download log file","The number of log files must be a positive integer")
def DeleteLog():
    validate = ValidateNumber(fileaged.get())
    if validate:
        if askyesno("Delete log files","Are you sure you want to delete the chosen log files?"):
            try: showinfo("Delete log files",GetData(GetCurrentDeviceIP(),"/deletelogs",postlist=[["lognum",lognumd.get()],["fileage",fileaged.get()],["app","1"]]).split("\r\n\r\n")[1])
            except ConnectionRefusedError: showerror("Shutdown",devsel.get() + " could not be reached")
    else:
        showerror("Delete log filed","The number of log files must be a positive integer")
def ShutDown():
    if askyesno("Shut down","Are you sure you want to shut down?"):
        try: showinfo("Shut down",GetData(GetCurrentDeviceIP(),"/shutdown",postlist=[["devices",sddevice.get()],["web",sdweb.get()],["app","1"]]).split("\r\n\r\n")[1])
        except ConnectionRefusedError: showerror("Shutdown",devsel.get() + " could not be reached")
def AddMenubarCommands(menu,commands):
    for command in commands:
        if len(command) == 2: menu.add_command(label=command[0],command=command[1])
        else: menu.add_separator()
def Settings():
    page = Toplevel()
    page.title("On/Off Monitor Settings")
    page.resizable(0,0)
    Label(page,text="Settings",font=fonts.h1).grid(row=1,column=1,columnspan=3)
    Label(page,text="Devices",font=fonts.h2).grid(row=2,column=1,columnspan=3)
    devicelist = Listbox(page)
    devicelist.grid(row=3,column=1,columnspan=3)
    Button(page,text="Add new",command=lambda:AddDevice(devicelist)).grid(row=4,column=1)
    Button(page,text="Remove selected",command=lambda:RemoveDevice(devicelist,page)).grid(row=4,column=3)
    Button(page,text="Set as default device",command=lambda:SetDefaultDevice(devicelist,page)).grid(row=4,column=2)
    for i in range(len(settings["devices"])): devicelist.insert(i,FormatDeviceName(i))
    page.mainloop()
def AddDevice(listbox):
    newname = askstring("Add device","Please enter the name of the new device")
    if newname != None and newname != "":
        newip = askstring("Add device","Please enter the IP address with port number (if required) of "+newname)
        if ValidateIPAddress(newip):
            settings["devices"].append([newname,newip])
            listbox.insert(len(settings["devices"]),newname+" ("+newip+")")
            SaveSettings(settings)
            devicemenu["menu"].add_command(FormatDeviceName(len(settings["devices"])-1))
def RemoveDevice(listbox,window):
    index=listbox.curselection()
    if len(index)>0:
        index=index[0]
        if askyesno("Remove device","Are you sure you want to delete "+listbox.get(index)+"?",parent=window):
            deleted = settings["devices"].pop(index)
            listbox.delete(index)
            devicemenu["menu"].delete(index)
            if deleted[1] == settings["defaultip"]:
                if len(settings["devices"])==0: settings["defaultip"]=""
                else: settings["defaultip"]=settings["devices"][0][1]
            CheckDefaultDevice()
            SaveSettings(settings)
def LogFileList():
    device = devsel.get()
    page = Toplevel()
    page.title(device + " log files - On/Off Monitor")
    page.resizable(0,0)
    Label(page,text=device + " log files").grid(row=1,column=1,columnspan=3)
    devicelist = Listbox(page)
    devicelist.grid(row=2,column=1,columnspan=3)
    Button(page,text="Refresh",command=lambda:RefreshLogFileList(device,devicelist)).grid(row=3,column=1)
    Button(page,text="Delete",command=lambda:DeleteLogFile(device,devicelist,page)).grid(row=3,column=2)
    Button(page,text="Open",command=lambda:OpenLogFile(device,devicelist)).grid(row=3,column=3)
    RefreshLogFileList(device,devicelist)
    page.mainloop()
def RefreshLogFileList(device,listbox):
    data = GetData(DeviceIPAddress(device),"/logfilelist",postlist=[["app","1"]])
    listbox.delete(0,"end")
    for i in range(len(data)):
        listbox.add(i,data[i][:4] + "/" + data[i][4:6] + "/" + data[i][6:8])
def DeleteLogFile(device,listbox,window):
    index = listbox.curselection()
    if len(index)>0:
        index=index[0]
        if askyesno("Delete log files","Are you sure you want to delete "+listbox.get(index)+"?",parent=window):
            showinfo("Delete log files",GetData(DeviceIPAddress(device,"/deletelogfile",postlist=[["app","1"],["lognum",str(index)]])))
            listbox.delete(index)
def OpenLogFile(device,listbox):
    index = listbox.curselection()
    if len(index)>0:
        index = index[0]
        data = GetData(DeviceIPAddress(device),"/logfile",postlist=[["lognum",str(index)],["app","1"]])
        print(ListToCsv(data.split("\r\n\r\n")[1]))
def SetDefaultDevice(listbox,window):
    index=listbox.curselection()
    if len(index)>0:
        index=index[0]
        settings["defaultip"]=index
        devsel.set(FormatDeviceName(index))
        SaveSettings(settings)
        showinfo("On/Off Monitor Settings",FormatDeviceName(index) + " was set as the default device",parent=window)
def FormatDeviceName(index): return settings["devices"][index][0]+" ("+settings["devices"][index][1]+")"
def DeviceIPAddress(device): return device.split("(")[1].split(")")[0]
def CheckDefaultDevice():
    if settings["defaultip"] not in range(len(settings["devices"])):
        if len(settings["devices"]) == 0:
            settings["defaultip"] = None
            devsel.set("(No devices)")
            showinfo("On/Off Monitor","No devices have been set up. Please go to Options > Settings and set up at least one On/Off Monitor device.")
        else:
            settings["defaultip"] = 0
            devsel.set(FormatDeviceName(0))
settings=GetSettings()
window = Tk()
window.title("On/Off Monitor")
menubar = Menu(window)
window.config(menu = menubar)
optionsmenu = Menu(menubar, tearoff = 0)
AddMenubarCommands(optionsmenu,[("Settings",Settings),(),("Exit",window.destroy)])
menubar.add_cascade(label="Options", menu=optionsmenu)

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
Button(window,text="Log file list",command=LogFileList).grid(row=5,column=3)

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
Radiobutton(window,text="Delete ^ of the oldest files",variable=fileaged,value="old",font=fonts.p).grid(row=10,column=1)
Radiobutton(window,text="Keep ^ of the newest files",variable=fileaged,value="new",font=fonts.p).grid(row=11,column=1)
Button(window,text="Delete",command=DeleteLog,font=fonts.p).grid(row=12,column=1)

Label(window,text="Shutdown",font=fonts.h2).grid(row=2,column=2,rowspan=2)
Radiobutton(window,text="This device",variable=sddevice,value="this",font=fonts.p).grid(row=4,column=2)
Radiobutton(window,text="All devices",variable=sddevice,value="all",font=fonts.p).grid(row=5,column=2)
Radiobutton(window,text="Web service",variable=sdweb,value="web",font=fonts.p).grid(row=6,column=2)
Radiobutton(window,text="Web service and device",variable=sdweb,value="all",font=fonts.p).grid(row=7,column=2)
Button(window,text="Shut down",command=ShutDown,font=fonts.p).grid(row=8,column=2)
CheckDefaultDevice()
window.mainloop()
