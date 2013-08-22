from time import time
from push import Pusher

START = None
line = "="*40
pusher = Pusher()


def log (msg, elapsed=None):
    pusher.addstyle("="*34)
    pusher.addstyle(msg)
    if elapsed:
        pusher.addstyle("Elapsed time: " + elapsed)
    pusher.addstyle("="*34)
    pusher.add("<br />")
    pusher.push()


def format_time(t):
    output = ""
    minutes = t/60
    seconds = t%60

    output += "%d minutes, " % minutes
    output += "{0:.3f} seconds".format(seconds)

    return output


def start():
    global START
    START = time()
    log("Start of Evolution")

    return START


def end():
    end = time()
    elapsed = end-START
    log("End of Evolution", format_time(elapsed))

    return end


def now():
    return format_time(time())
