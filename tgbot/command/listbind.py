
from tgbot.command import Command

class ListBind(Command):

    def __init__(self, cmd):
        super(ListBind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, msg):
        _chat = msg['chat']
        message = ''
        for each in bot.tunnels:
            message += 'TG: {0} <-> TK: {1}\n'.format(each.tg['id'], each.tk['id'])
        if message == '':
            message = 'No existing binding.'
        bot.sendMessage(_chat['id'], message)

