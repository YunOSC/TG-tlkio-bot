
class Alarm(Command):

    def __init__(self, cmd, alarmTS):
        super(Alarm, self).__init__(cmd, alarmTS)

    def invoke(self, msg):
        pass

    def process(self, bot, cmd, msg):
        pass
