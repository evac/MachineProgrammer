from time import time
from push import Pusher

START = None
line = "="*40
pusher = Pusher()

def log (msg, elapsed=None):
    print line
    print msg
    if elapsed:
        print "Elapsed time:", elapsed
    print line
    print

    pusher.addstyle("="*34)
    pusher.addstyle(msg)
    if elapsed:
        pusher.addstyle("Elapsed time: " + elapsed)
    pusher.addstyle("="*34)
    pusher.add("<br />")
    pusher.push()


def now():
    return format_time(time())

def format_time(t):
    time = ""

    minutes = t/60
    seconds = t%60

    time += "%d minutes, " % minutes
    time += "{0:.3f} seconds".format(seconds)

    return time

def endlog():
    end = time()
    elapsed = end-START
    log("End of Evolution", format_time(elapsed))

def start():
    global START
    START = time()
    log("Start of Evolution")

def end():
    endlog()