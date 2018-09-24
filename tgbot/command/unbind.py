
from tgbot.command import Command

class UnBint(object):

    def __init__(self, cmd):
        super(UnBind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, msg):
        _chat = msg['chat']
        _text = msg['text']
        tkNames = _text.replace('/unbind ', '').split(' ')
        if tkNames = []:
        else:
            for each in tkNames:
                bot.tunnels.        
