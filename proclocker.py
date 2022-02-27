import psutil
import os

proclock = True

def status():
    
    while proclock:
        reopen_A8 = True
        for proc in psutil.process_iter():
            if proc.name() == "actividad08.exe":
                reopen_A8 = False

        if reopen_A8:
            os.startfile('actividad08.exe')

status()