from OnOffMonitor import *
try:
    from tkinter import *
    from tkinter.filedialog import asksaveasfile
except ModuleNotFoundError:
    from Tkinter import *
    from tkFileDialog import asksaveasfile
def DownloadLog():
    f = asksaveasfile(title="Save log file as...",defaultextension=".csv",filetypes=[("Comma-separated values format","*.csv")])
    if f != None:
        test=GetData(settings.devices[0],"/log.csv?lognum="+lognumdl.get()+"&fileage="+fileagedl.get())
        print(test)
        f.write(test)
        f.close()
def DeleteLog():
    pass
window = Tk()
window.title("On/Off Monitor")
window.resizable(0,0)
fileagedl = StringVar() #Fileage for download logs
fileaged = StringVar() #Fileage for delete logs
fileagedl.set("new")
fileaged.set("old")
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
Radiobutton(window,text="Delete ^ of the oldest files",variable=fileaged,value="old").grid(row=9,column=1)
Radiobutton(window,text="Keep ^ of the newest files",variable=fileaged,value="new").grid(row=10,column=1)
Button(window,text="Delete",command=DeleteLog).grid(row=11,column=1)
window.mainloop()
