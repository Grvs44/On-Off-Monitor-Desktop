import subprocess
import sys
print("Installing On/Off Monitor Desktop...")
subprocess.Popen([sys.executable, "-m", "pip", "install", "onoffmonitordesktop-1.1.4-py2.py3-none-any.whl", "--upgrade"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
startshortcut = "y" in input("Create a shortcut in the Start menu? (y/n)").lower()
desktopshortcut = "y" in input("Create a desktop shortcut? (y/n)").lower()
if startshortcut or desktopshortcut:
    subprocess.Popen([sys.executable, "-m", "pip", "install", "pyshortcuts"],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    import OnOffMonitorDesktop as module
    from pyshortcuts import make_shortcut
    import os.path
    make_shortcut(os.path.join(os.path.dirname(module.__file__)),name='On-Off Monitor Desktop',desktop=desktopshortcut,startmenu=startshortcut,terminal=False)
input("On/Off Monitor Desktop has finished installing. Press RETURN to exit ")
