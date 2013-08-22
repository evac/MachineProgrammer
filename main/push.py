import pusher

p = pusher.Pusher(
  app_id='52211',
  key='9eb76d1f686de8651d46',
  secret='975144a7f85eced304f6'
)

class Pusher(object):
    def __init__(self, event="log"):
        self.channel = 'evolution'
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
        p[self.channel].trigger('logs', data)

        # reset message
        self.message = ""