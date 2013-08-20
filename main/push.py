import pusher

p = pusher.Pusher(
  app_id='52196',
  key='2049f32f18b0865b213e',
  secret='4aca3297f89652b562ee'
)

class Pusher(object):
    def __init__(self, event="log"):
        self.channel = 'evolution'
        self.message = ""
        self.event = event

    def addstyle(self, msg):
        self.message += "<span>" + msg + "</span>"

    def add(self, msg):
        self.message += msg

    def push(self, msg=""):
        self.message += msg
        data = {}

        if self.event == "output":
            data = {'output': self.message}
        else:
            data = {'log': self.message}

        p[self.channel].trigger('logs', data)
        self.message = ""