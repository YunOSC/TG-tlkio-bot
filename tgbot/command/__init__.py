
class Command(object):

    def __init__(self, cmd, invoke=False, **kwargs):
        self.cmd = cmd
        self.invoke = invoke
        for (key, value) in kwargs.items():
            setattr(key, value)

    def invoke(self, msg):
        raise NotImplementedError

    def process(self, **kwargs):
        raise NotImplementedError


