
from tgbot.command import Command

class ListBind(Command):

    def __init__(self, cmd):
        super(ListBind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, cmd, msg):
        _tgId = msg['chat']['id']
        message = ''
        if len(cmd) > 1:
            target = cmd[1]
            if target == 'global':
                for each in bot.tunnels:
                    message += 'TG: {0} <-> TK: {1}/{2}\n'.format(each.tg['id'], each.tk['id'], each.tk['name'])
        else:
            for each in bot.tunnels:
                if each.tg['id'] == _tgId:
                    message += 'TG: {0} <-> TK: {1}/{2}\n'.format(each.tg['id'], each.tk['id'], each.tk['name'])
        
        if message == '':
            message = 'No existing binding.'
        bot.sendMessage(_tgId, message)

