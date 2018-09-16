
class Command(object):

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        for (key, value) in kwargs.items():
            setattr(key, value)


