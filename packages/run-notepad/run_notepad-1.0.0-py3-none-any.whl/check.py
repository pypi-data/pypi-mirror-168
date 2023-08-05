import psutil
import subprocess
import threading

from urllib.request import urlopen

def check_exe():
    if (threading.current_thread().is_alive()):
        threading.enumerate()
    threading.Timer(10.0, check_exe).start()
    if "notepad.exe" in (p.name() for p in psutil.process_iter()):
        print("exist")
    else:
        print("no exist")
        subprocess.call("C:\\Windows\\notepad.exe")


def is_connected():
   try:
        response = urlopen('https://www.google.com/', timeout=5)
        if (threading.current_thread().is_alive()):
            threading.enumerate()
        print("internet on")
        threading.Timer(10.0, check_exe).start()

   except:
       print("internet off")
       if (threading.current_thread().is_alive()):
        threading.enumerate()
       threading.Timer(10.0, is_connected).start()

is_connected()






