from OnOffMonitor import *
try:
    from tkinter import Tk,StringVar,Label,Entry,Button,Radiobutton,Menu,Toplevel,Listbox
    from tkinter.filedialog import asksaveasfile
    from tkinter.messagebox import showinfo,askyesno,showerror
    from tkinter.simpledialog import askstring
except ModuleNotFoundError:
    from Tkinter import Tk,StringVar,Label,Entry,Button,Radiobutton,Menu,Toplevel,Listbox
    from tkFileDialog import asksaveasfile
    from tkMessageBox import showinfo,askyesno,showerror
    from tkSimpleDialog import askstring
def DownloadLog():
    validate = ValidateNumber(fileagedl.get())
    if validate:
        f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")])
        if f != None:
            try:
                f.write(GetData(devices[0],"/log.csv",postlist=[["lognum",lognumdl.get()],["fileage",fileagedl.get()]]).split("\r\n\r\n")[1])
                f.close()
                showinfo("Download log file","Log file downloaded to " + f.name)
            except ConnectionRefusedError: showerror("Download log file","Error: the device at " + devices[0] + " could not be reached")
    else:
        showerror("Download log file","The number of log files must be a positive integer")
def DeleteLog():
    validate = ValidateNumber(fileaged.get())
    if validate:
        if askyesno("Delete log files","Are you sure you want to delete the chosen log files?"):
            try: showinfo("Delete log files",GetData(devices[0],"/deletelogs",postlist=[["lognum",lognumd.get()],["fileage",fileaged.get()],["app","1"]]).split("\r\n\r\n")[1])
            except ConnectionRefusedError: showerror("Shutdown","Error: the device at " + devices[0] + " could not be reached")
    else:
        showerror("Delete log filed","The number of log files must be a positive integer")
def ShutDown():
    if askyesno("Shut down","Are you sure you want to shut down?"):
        try: showinfo("Shut down",GetData(devices[0],"/shutdown",postlist=[["devices",sddevice.get()],["web",sdweb.get()],["app","1"]]).split("\r\n\r\n")[1])
        except ConnectionRefusedError: showerror("Shutdown","Error: the device at " + devices[0] + " could not be reached")
def AddMenubarCommands(menu,commands):
    for command in commands:
        if len(command) == 2: optionmenu.add_command(label=command[0],command=command[1])
        else: menu.add_separator()
def Settings():
    page = Toplevel()
    page.title("On/Off Monitor Settings")
    page.resizable(0,0)
    Label(page,text="Settings",font=fonts.h1).grid(row=1,column=1,columnspan=2)
    Label(page,text="Devices",font=fonts.h2).grid(row=2,column=1,columnspan=2)
    devicelist = Listbox(page)
    devicelist.grid(row=3,column=1,columnspan=2)
    Button(page,text="Add new").grid(row=4,column=1)
    Button(page,text="Remove selected").grid(row=4,column=2)
    for i in range(len(devices)): devicelist.add(i,devices[i])
    page.mainloop()
def AddDevice(listbox):
    newip = askstring("Add device","Please enter the IP address with port number (if required) of the new device")
    if ValidateIPAddress(newip):
        devices.append(newip)
        listbox.add(len(devices),newip)
devices=GetSettings()
window = Tk()
window.title("On/Off Monitor")
menubar = Menu(window)
window.config(menu = menubar)
optionmenu = Menu(menubar, tearoff = 0)
AddMenubarCommands(optionmenu,[("Settings",Settings),(),("Exit",window.destroy)])
menubar.add_cascade(label="Options", menu=optionmenu)

fileagedl = StringVar() #Fileage for download logs
fileaged = StringVar() #Fileage for delete logs
sddevice = StringVar() #Shut down this or all devices
sdweb = StringVar() #Shut down web or devices
fileagedl.set("new")
fileaged.set("old")
sddevice.set("this")
sdweb.set("web")

Label(window,text="Log files",font=fonts.h1).grid(row=1,column=1)
Label(window,text="Download",font=fonts.h2).grid(row=2,column=1)
lognumdl = Entry(window,font=fonts.p)
lognumdl.grid(row=3,column=1)
Radiobutton(window,text="of the oldest files",variable=fileagedl,value="old",font=fonts.p).grid(row=4,column=1)
Radiobutton(window,text="of the newest files",variable=fileagedl,value="new",font=fonts.p).grid(row=5,column=1)
Button(window,text="Download",command=DownloadLog,font=fonts.p).grid(row=6,column=1)

Label(window,text="Delete",font=fonts.h2).grid(row=7,column=1)
lognumd = Entry(window,font=fonts.p)
lognumd.grid(row=8,column=1)
Radiobutton(window,text="Delete ^ of the oldest files",variable=fileaged,value="old",font=fonts.p).grid(row=9,column=1)
Radiobutton(window,text="Keep ^ of the newest files",variable=fileaged,value="new",font=fonts.p).grid(row=10,column=1)
Button(window,text="Delete",command=DeleteLog,font=fonts.p).grid(row=11,column=1)

Label(window,text="Shutdown",font=fonts.h1).grid(row=1,column=2,rowspan=2)
Radiobutton(window,text="This device",variable=sddevice,value="this",font=fonts.p).grid(row=3,column=2)
Radiobutton(window,text="All devices",variable=sddevice,value="all",font=fonts.p).grid(row=4,column=2)
Radiobutton(window,text="Web service",variable=sdweb,value="web",font=fonts.p).grid(row=5,column=2)
Radiobutton(window,text="Web service and device",variable=sdweb,value="all",font=fonts.p).grid(row=6,column=2)
Button(window,text="Shut down",command=ShutDown,font=fonts.p).grid(row=7,column=2)
window.mainloop()
