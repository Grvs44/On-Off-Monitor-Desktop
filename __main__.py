from OnOffMonitor import *
from time import sleep
class Home:
    def __init__(this):
        this.window = Tk()
        this.window.title("On/Off Monitor")
        menubar = Menu(this.window,font=fonts.p)
        this.window.config(menu = menubar)
        optionsmenu = Menu(menubar, tearoff = 0)
        AddMenubarCommands(optionsmenu,[("Settings",Settings),(),("Exit",this.window.destroy)])
        menubar.add_cascade(label="Options", menu=optionsmenu)

        this.window.grid_columnconfigure(1,weight=1)
        this.window.grid_columnconfigure(2,weight=1)
        this.window.grid_columnconfigure(3,weight=1)

        this.fileagedl = StringVar() #Fileage for download logs
        this.fileaged = StringVar() #Fileage for delete logs
        this.sddevice = StringVar() #Shut down this or all devices
        this.sdweb = StringVar() #Shut down web or devices
        this.devsel = StringVar() #Variable to chose device to send/receive requests
        this.fileagedl.set("new")
        this.fileaged.set("old")
        this.sddevice.set("this")
        this.sdweb.set("web")
        Label(this.window,text="On/Off Monitor",font=fonts.h1).grid(row=1,column=1,columnspan=3)
        Label(this.window,text="Devices",font=fonts.h2).grid(row=2,column=3,rowspan=2)
        devicemenuitems = []
        for device in settings["devices"]:
            devicemenuitems.append(device[0] + " (" + device[1] + ")")
        if len(devicemenuitems) == 0:
            devicemenuitems.append("(No devices)")
        this.devicemenu = OptionMenu(this.window,this.devsel,*devicemenuitems)
        this.devicemenu.grid(row=4,column=3)
        Button(this.window,text="Log file list",command=LogFileList,font=fonts.p).grid(row=5,column=3)

        Label(this.window,text="Log files",font=fonts.h2).grid(row=2,column=1)
        Label(this.window,text="Download",font=fonts.h3).grid(row=3,column=1)
        this.lognumdl = Entry(this.window,font=fonts.p)
        this.lognumdl.grid(row=4,column=1)
        Radiobutton(this.window,text="of the oldest files",variable=this.fileagedl,value="old",font=fonts.p).grid(row=5,column=1)
        Radiobutton(this.window,text="of the newest files",variable=this.fileagedl,value="new",font=fonts.p).grid(row=6,column=1)
        Button(this.window,text="Download",command=this.DownloadLog,font=fonts.p).grid(row=7,column=1)

        Label(this.window,text="Delete",font=fonts.h3).grid(row=8,column=1)
        this.lognumd = Entry(this.window,font=fonts.p)
        this.lognumd.grid(row=9,column=1)
        this.delrad1 = Radiobutton(this.window,text="Delete ^ of the oldest files",variable=this.fileaged,value="old",font=fonts.p)
        this.delrad1.grid(row=10,column=1)
        this.delrad2 = Radiobutton(this.window,text="Keep ^ of the newest files",variable=this.fileaged,value="new",font=fonts.p)
        this.delrad2.grid(row=11,column=1)
        Button(this.window,text="Delete",command=this.DeleteLog,font=fonts.p).grid(row=12,column=1)
        this.lognumd.bind("<KeyRelease>",this.UpdateDeleteText)

        Label(this.window,text="Shutdown",font=fonts.h2).grid(row=2,column=2,rowspan=2)
        Radiobutton(this.window,text="This device",variable=this.sddevice,value="this",font=fonts.p).grid(row=4,column=2)
        Radiobutton(this.window,text="All devices",variable=this.sddevice,value="all",font=fonts.p).grid(row=5,column=2)
        Radiobutton(this.window,text="On/Off Monitor",variable=this.sdweb,value="web",font=fonts.p).grid(row=6,column=2)
        Radiobutton(this.window,text="On/Off Monitor and device",variable=this.sdweb,value="all",font=fonts.p).grid(row=7,column=2)
        Button(this.window,text="Shut down",command=this.ShutDown,font=fonts.p).grid(row=8,column=2)

        Button(this.window,text="Live Device Status",font=fonts.p,command=Status).grid(row=8,column=3)
        Button(this.window,text="Test pins",font=fonts.p,command=TestPins).grid(row=9,column=3)
        if this.CheckDefaultDevice(): showinfo("On/Off Monitor","No devices have been set up. Please go to Options > Settings and set up at least one On/Off Monitor device.")
    def DownloadLog(this):
        if this.devsel.get() == "(No devices)": return
        if ValidateNumber(this.lognumdl.get()):
            f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")],parent=this.window)
            if f != None:
                try:
                    f.write(GetData(DeviceIPAddress(this.devsel.get()),"/log.csv",postlist=[["lognum",this.lognumdl.get()],["fileage",this.fileagedl.get()]]).split("\r\n\r\n")[1])
                    f.close()
                    showinfo("Download log file","Log file downloaded to " + f.name)
                except ConnectionRefusedError: ConnectionRefused(this.devsel.get(),this.window)
        else:
            showerror("Download log file","The number of log files must be a positive integer",parent=this.window)
    def DeleteLog(this):
        if this.devsel.get() == "(No devices)": return
        if ValidateNumber(this.lognumd.get()):
            if askyesno("Delete log files","Are you sure you want to delete the chosen log files?"):
                try: showinfo("Delete log files",GetData(DeviceIPAddress(this.devsel.get()),"/deletelogs",postlist=[["lognum",this.lognumd.get()],["fileage",this.fileaged.get()],["app","1"]]).split("\r\n\r\n")[1])
                except ConnectionRefusedError: ConnectionRefused(this.devsel.get(),this.window)
        else:
            showerror("Delete log files","The number of log files must be a positive integer",parent=this.window)
    def ShutDown(this):
        if this.devsel.get() == "(No devices)": return
        if askyesno("Shut down","Are you sure you want to shut down?"):
            try: showinfo("Shut down",GetData(DeviceIPAddress(this.devsel.get()),"/shutdown",postlist=[["devices",this.sddevice.get()],["web",this.sdweb.get()],["app","1"]]).split("\r\n\r\n")[1])
            except ConnectionRefusedError: ConnectionRefused(this.devsel.get(),this.window)
    def CheckDefaultDevice(this,updated=False):
        if updated or settings["defaultip"] not in range(len(settings["devices"])):
            if len(settings["devices"]) == 0:
                settings["defaultip"] = None
                this.devsel.set("(No devices)")
                return True
            else:
                settings["defaultip"] = 0
                this.devsel.set(FormatDeviceName(0))
        else:
            this.devsel.set(FormatDeviceName(settings["defaultip"]))
    def UpdateDeleteText(this,e):
        this.delrad1.config(text="Delete "+this.lognumd.get()+" of the oldest files")
        this.delrad2.config(text="Keep "+this.lognumd.get()+" of the newest files")
def AddMenubarCommands(menu,commands):
    for command in commands:
        if len(command) == 2: menu.add_command(label=command[0],command=command[1])
        else: menu.add_separator()

class Settings:
    def __init__(this):
        this.window = Toplevel()
        this.window.title("On/Off Monitor Settings")
        this.window.grid_rowconfigure(4,weight=1)
        this.window.grid_columnconfigure(1,weight=1)
        this.window.grid_columnconfigure(2,weight=1)
        this.window.grid_columnconfigure(3,weight=1)
        Label(this.window,text="Settings",font=fonts.h1).grid(row=1,column=1,columnspan=3,sticky="NSEW")
        Label(this.window,text="This device ID",font=fonts.p).grid(row=2,column=1,sticky="NSE")
        this.deviceid = Entry(this.window,font=fonts.p)
        this.deviceid.grid(row=2,column=2,sticky="NSEW")
        this.deviceid.insert(0,settings["id"])
        Button(this.window,text="Save",font=fonts.p,command=this.SaveDeviceId).grid(row=2,column=3,sticky="NSW")
        Label(this.window,text="Devices",font=fonts.h2).grid(row=3,column=1,columnspan=3,sticky="NSEW")
        this.devicelist = Listbox(this.window,font=fonts.p,selectmode="multiple")
        scroll_v = Scrollbar(this.window,command=this.devicelist.yview)
        scroll_h = Scrollbar(this.window,command=this.devicelist.xview,orient="horizontal")
        this.devicelist.config(xscrollcommand=scroll_h.set,yscrollcommand=scroll_v.set)
        scroll_v.grid(row=4,column=4,sticky="NSEW")
        scroll_h.grid(row=5,column=1,columnspan=3,sticky="NSEW")
        this.devicelist.grid(row=4,column=1,columnspan=3,sticky="NSEW")
        Button(this.window,text="Add new",font=fonts.p,command=this.AddDevice).grid(row=6,column=1)
        Button(this.window,text="Remove selected",font=fonts.p,command=this.RemoveDevice).grid(row=6,column=3)
        Button(this.window,text="Set as default device",font=fonts.p,command=this.SetDefaultDevice).grid(row=6,column=2)
        for i in range(len(settings["devices"])): this.devicelist.insert(i,FormatDeviceName(i))
        if settings["defaultip"] != None: this.devicelist.itemconfig(i,bg="#f0f0f0")
        this.window.mainloop()
    def AddDevice(this):
        newname = askstring("Add device","Please enter the name of the new device")
        if newname != None and newname != "":
            newip = askstring("Add device","Please enter the IP address with port number (if required) of "+newname)
            if ValidateIPAddress(newip):
                settings["devices"].append([newname,newip])
                this.devicelist.insert(len(settings["devices"]),newname+" ("+newip+")")
                SaveSettings()
                if len(settings["devices"]) == 1:
                    home.devicemenu["menu"].delete(0)
                    settings["defaultip"] = 0
                    home.devsel.set(newname + " (" + newip + ")")
                home.devicemenu["menu"].add_command(label=newname+" ("+newip+")")
    def RemoveDevice(this):
        index = this.devicelist.curselection()
        if len(index)>0:
            if askyesno("Remove device","Are you sure you want to delete the selected devices?",parent=this.window):
                deleted = "Removed device(s):"
                for i in range(len(index)-1,-1,-1):
                    delitem=settings["devices"].pop(index[i])
                    deleted += "\n" + delitem[0] + " (" + delitem[1] + ")"
                    this.devicelist.delete(index[i])
                    home.devicemenu["menu"].delete(index[i])
                if settings["defaultip"] in index:
                    home.CheckDefaultDevice(updated=True)
                    if len(settings["devices"]) == 0:
                        home.devicemenu["menu"].add_command(label="(No devices)")
                    else:
                        settings["defaultip"] = 0
                        deleted+="\nSet "+FormatDeviceName(0)+" as the default device"
                        this.devicelist.itemconfig(0,bg="#f0f0f0")
                SaveSettings()
                showinfo("Remove device",deleted,parent=this.window)
    def SaveDeviceId(this):
        settings["id"] = this.deviceid.get()
        SaveSettings()
        showinfo("On/Off Monitor Settings","Updated this device's ID",parent=this.window)
    def SetDefaultDevice(this):
        index = this.devicelist.curselection()
        if len(index)>0:
            index = index[0]
            this.devicelist.itemconfig(settings["defaultip"],bg="#ffffff")
            settings["defaultip"] = index
            home.devsel.set(FormatDeviceName(index))
            this.devicelist.itemconfig(index,bg="#f0f0f0")
            SaveSettings()
            showinfo("On/Off Monitor Settings",FormatDeviceName(index) + " was set as the default device",parent=this.window)

class LogFileList():
    def __init__(this):
        this.device = home.devsel.get()
        if this.device == "(No devices)": return
        this.page = Toplevel()
        this.page.title(this.device + " log files - On/Off Monitor")
        this.page.grid_rowconfigure(2,weight=1)
        this.page.grid_columnconfigure(1,weight=1)
        this.page.grid_columnconfigure(2,weight=1)
        this.page.grid_columnconfigure(3,weight=1)
        Label(this.page,text=this.device + " log files",font=fonts.h1).grid(row=1,column=1,columnspan=4,sticky="NSEW")
        this.devicelist = Listbox(this.page,font=fonts.p,selectmode="multiple")
        scroll_v = Scrollbar(this.page,command=this.devicelist.yview)
        scroll_h = Scrollbar(this.page,command=this.devicelist.xview,orient="horizontal")
        this.devicelist.config(xscrollcommand=scroll_h.set,yscrollcommand=scroll_v.set)
        scroll_v.grid(row=2,column=4,sticky="NSEW")
        scroll_h.grid(row=3,column=1,columnspan=3,sticky="NSEW")
        this.devicelist.grid(row=2,column=1,columnspan=3,sticky="NSEW")
        Button(this.page,text="Refresh",font=fonts.p,command=this.RefreshLogFileList).grid(row=4,column=1)
        Button(this.page,text="Delete",font=fonts.p,command=this.DeleteLogFile).grid(row=4,column=2)
        Button(this.page,text="Open",font=fonts.p,command=this.OpenLogFile).grid(row=4,column=3)
        this.RefreshLogFileList()
        if this.devicelist.size() == 0: this.page.destroy()
        this.page.mainloop()
    def RefreshLogFileList(this):
        try:
            data = loads(GetBody(GetData(DeviceIPAddress(this.device),"/logfilelist",postlist=[["app","1"]])))
            this.devicelist.delete(0,"end")
            for i in range(len(data)): this.devicelist.insert(i,data[i][:4] + "/" + data[i][4:6] + "/" + data[i][6:8])
        except ConnectionRefusedError: ConnectionRefused(this.device,home.window)
    def DeleteLogFile(this):
        if len(this.devicelist.curselection())>0:
            if askyesno("Delete log files","Are you sure you want to delete the selected items?",parent=this.page):  
                response=""
                index=list(this.devicelist.curselection())
                for i in range(len(index)-1,-1,-1):
                    try:
                        response+=GetBody(GetData(DeviceIPAddress(this.device),"/deletelocallog",postlist=[["app","1"],["lognum",str(index[i])]]))+"\n"
                        this.devicelist.delete(index[i])
                    except ConnectionRefusedError: ConnectionRefused(this.device,home.window)
                showinfo("Delete log files",response,parent=this.page)
    def OpenLogFile(this):
        selection = this.devicelist.curselection()
        if len(selection)>0:
            f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")])
            if f != None:
                try:
                    data=[]
                    for index in selection: data.extend(loads(GetBody(GetData(DeviceIPAddress(this.device),"/logfile",[["lognum",str(index)],["app","1"]]))))
                    f.write(ListToCsv("Date,Time,Device,Status",data))
                    showinfo("Open log file","Log file saved to "+f.name)
                except ConnectionRefusedError: ConnectionRefused(this.device,home.window)
                f.close()
def ConnectionRefused(device,window): showerror("On/Off Monitor",device + " could not be reached. Please check that it is running On/Off Monitor and connected to the same network.",parent=window)

# LiveStatus
class Status:
    def __init__(this):
        if home.devsel.get() == "(No devices)": return
        this.ipaddress = DeviceIPAddress(home.devsel.get())
        if not ValidateIPAddress(this.ipaddress):
            showerror("Live Device Status - On/Off Monitor","Invalid IP Address",parent=home.window)
            return
        from threading import Thread
        this.win = Tk()
        this.win.title("Live Device Status - On/Off Monitor")
        this.win.grid_columnconfigure(1,weight=1)
        this.win.grid_columnconfigure(2,weight=1)
        this.win.grid_rowconfigure(4,weight=1)
        this.table = [Listbox(this.win,font=fonts.p,selectmode="none",justify="center"),Listbox(this.win,font=fonts.p,selectmode="none",justify="center")]
        this.refresh = Entry(this.win,text="10")
        Label(this.win,text="Live Device Status",font=fonts.h1).grid(row=1,column=1,columnspan=3,sticky="NSEW")
        Label(this.win,text="Refresh period (sec)",font=fonts.p).grid(row=2,column=1,sticky="NSE")
        this.refresh.grid(row=2,column=2,sticky="NSW")
        this.refresh.insert(0,"10")
        Label(this.win,text="Name",font=fonts.h2).grid(row=3,column=1,sticky="NSEW")
        Label(this.win,text="Status",font=fonts.h2).grid(row=3,column=2,sticky="NSEW")
        this.table[0].grid(row=4,column=1,sticky="NSEW")
        this.table[1].grid(row=4,column=2,sticky="NSEW")
        Thread(target=this.RequestStatus).start()
        this.win.mainloop()
    def RequestStatus(this):
        try:
            while True:
                this.table[0].delete(0,END)
                this.table[1].delete(0,END)
                data = loads(GetBody(GetData(this.ipaddress,"/status/status.json")))
                for i in range(len(data)):
                    for j in [0,1]:
                        this.table[j].insert(i,data[i][j])
                sleep(this.sleeptime())
        except TclError: pass # When win closes and window is still open
        except RuntimeError: pass # When win closes and window is already closed
        except ConnectionRefusedError:
            ConnectionRefused(this.devsel.get(),this.win)
            this.win.destroy()
    def sleeptime(this):
        try:
            number = float(this.refresh.get())
            if number < 0.05: return 10
            else: return number
        except ValueError: return 10

class TestPins:
    def __init__(this):
        if home.devsel.get() == "(No devices)": return
        this.ipaddress = DeviceIPAddress(home.devsel.get())
        try:
            this.pins = loads(GetBody(GetData(this.ipaddress,"/pinnames",[["id",settings["id"]]])))
            this.window = Toplevel()
            this.window.title("Test pins - On/Off Monitor (using ID \"" + settings["id"] + "\")")
            this.window.grid_columnconfigure(1,weight=1)
            this.window.grid_rowconfigure(2,weight=1)
            Label(this.window,text="Test pins",font=fonts.h1).grid(row=1,column=1,columnspan=2,sticky="NSEW")
            this.pinlist = Listbox(this.window,font=fonts.p)
            this.pinlist.grid(row=2,column=1,sticky="NSEW")
            scrolly = Scrollbar(this.window,command=this.pinlist.yview)
            scrollx = Scrollbar(this.window,command=this.pinlist.xview,orient="horizontal")
            scrolly.grid(row=2,column=2,sticky="NSEW")
            scrollx.grid(row=3,column=1,sticky="NSEW")
            this.pinlist.config(yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            this.pinstates = [False]*len(this.pins)
            for pin in this.pins:
                this.pinlist.insert("end",pin)
            this.pinlist.bind("<<ListboxSelect>>",this.SendPinRequest)
        except ConnectionRefusedError: ConnectionRefused(devsel.get(),home.window)
    def SendPinRequest(this,e):
        try:
            item = this.pinlist.curselection()[0]
            if GetBody(GetData(this.ipaddress,"/pinaccess",[["state","0" if this.pinstates[item] else "1"],["pin",this.pinlist.get(item).replace(" ","+")],["id",settings["id"]]])) == "1":
                this.pinstates[item] = not this.pinstates[item]
                if this.pinstates[item]:
                    this.pinlist.itemconfig(item,bg="#00e800",fg="#000000")
                else:
                    this.pinlist.itemconfig(item,bg="#ea0000",fg="#ffffff")
                this.pinlist.selection_clear(item)
            else:
                showerror("Test pins - On/Off Monitor","There was an error changing the state of this pin. Please check your connection to the On/Off Monitor device and that you are using a valid device ID",parent=this.window)
        except ConnectionRefusedError: ConnectionRefused(devsel.get(),this.window)
        except IndexError: pass

if __name__ == "__main__":
    home = Home()
    home.window.mainloop()
