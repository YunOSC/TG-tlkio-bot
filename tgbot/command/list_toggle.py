from telebot import TeleBot
from tgbot.command import Command

class ListToggle(Command):

    def __init__(self, bot, cmd):
        super(ListToggle, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        cmd = msg.text.split(' ')
        tunnel = cmd[1] if len(cmd) > 1 else 'all'
        message = ''

        for each in self.bot.tunnels:
            if tunnel == 'all' or each.tk['name'] == tunnel:
                if each.tg['toggle'] and each.tk['toggle']:
                    message += 'This TG room <===> Tk {0}\n'.format(each.tk['name'])
                elif each.tg['toggle'] and not each.tk['toggle']:
                    message += 'This TG room ----> Tk {0}\n'.format(each.tk['name'])
                elif not each.tg['toggle'] and each.tk['toggle']:
                    message += 'This TG room <---- Tk {0}\n'.format(each.tk['name'])
                else:
                    message += 'This TG room --x-- Tk {0}\n'.format(each.tk['name'])
        if message == '':
            message = 'No existing bind to show toggle status.'
        else:
            message = 'Toggled: \n' + message
        self.bot.sendMessage(_tgId, message)
