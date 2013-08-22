import pusher

APP_ID = None
KEY = None
SECRET = None
CHANNEL = None
PUSHER = None

def add_settings(settings):
    global APP_ID
    global KEY
    global SECRET
    global CHANNEL
    global PUSHER

    APP_ID = settings["app_id"]
    KEY = settings["key"]
    SECRET = settings["secret"]
    CHANNEL = settings["channel"]
    PUSHER = pusher.Pusher(APP_ID, KEY, SECRET)


class Pusher(object):
    def __init__(self, event="log"):
        self.channel = CHANNEL
        self.message = ""
        self.event = event

    def get(self):
        # return current message
        return self.message

    def addstyle(self, msg):
        # add message with span tags
        self.message += "<span>" + msg + "</span>"

    def add(self, msg):
        # add message plain
        self.message += msg

    def push(self, msg=""):
        self.message += msg
        data = {}

        # set event type
        if self.event == "output":
            data = {'output': self.message}
        else:
            data = {'log': self.message}

        # push message
        PUSHER[self.channel].trigger('logs', data)

        # reset message
        self.message = ""