
from telebot import TeleBot
from tgbot.command import Command

class ListBind(Command):

    def __init__(self, bot, cmd):
        super(ListBind, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        cmd = msg.text.split(' ')
        message = ''
        if len(cmd) > 1:
            target = cmd[1]
            if target == 'global':
                for each in self.bot.tunnels:
                    message += 'TG: {0} <-> TK: {1}/{2}\n'.format(each.tg['id'], each.tk['id'], each.tk['name'])
        else:
            for each in self.bot.tunnels:
                if each.tg['id'] == _tgId:
                    message += 'TG: {0} <-> TK: {1}/{2}\n'.format(each.tg['id'], each.tk['id'], each.tk['name'])
        
        if message == '':
            message = 'No existing binding.'
        self.bot.sendMessage(_tgId, message)

