from threading import*
from time import sleep

mypybag_clocks=[]
mypybag_threads=[]

class clock(Thread):
    def __init__(self,command,time=1/60):
        super().__init__(target=command)
        self.time=time
        self.target=command
        self.d=False
    def run(self):
        while True:
            if self.d:
                break
            sleep(self.time)
            self.target()
    def dead(self):
        self.d=True
            
def add_schedule(command,time=1/60):
    mypybag_clocks.append(clock(command,time))

def run_schedule():
    for c in mypybag_clocks:
        c.start()
    for c in mypybag_clocks:
        c.join()
def stop_all_schedule():
    for c in mypybag_clocks:
        c.dead()

class threading(Thread):
    def __init__(self,command):
        super().__init__(target=command)
        self.target=command
        self.d=False
    def run(self):
        self.target()

def add_thread(command):
    mypybag_threads.append(threading(command))

def run_thread():
    for t in mypybag_threads:
        t.start()

def run():
    for t in mypybag_threads:
        t.start()
    for c in mypybag_clocks:
        c.start()
    for c in mypybag_clocks:
        c.join()

def cancel():
    mypybag_threads.clear()
    mypybag_clocks.clear()

def cancel_schedule():
    mypybag_clocks.clear()

def cancel_thread():
    mypybag_threads.clear()
