
from utils import *
from tgbot.command import Command

class Toggle(Command):

    def __init__(self, bot, cmd):
        super(Toggle, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        cmd = msg.text.split(' ')
        if len(cmd) == 2:
            if cmd[1] in ['tk', 'tg', 'all']:
                tunnel = 'all'
                side = cmd[1]
            else:
                tunnel = cmd[1]
                side = 'all'
        elif len(cmd) >= 3:
            if cmd[1] in ['tk', 'tg']:
                return self.bot.sendMessage(_tgId, 'tk or tg can not as tinnel name.')
            elif cmd[2] in ['tk', 'tg', 'all']:
                tunnel = cmd[1]
                side = cmd[2]
            else:
                return self.bot.sendMessage(_tgId, 'choose tk, tg, or all to specific side.')
        else:
            side = 'all'
            tunnel = 'all'

        message = 'Toggled: \n'
#        for each in getMatchTunnels(self.bot.tunnels, tgId=_tgId):
        for each in self.bot.tunnels:
            if tunnel == 'all' or each.tk['name'] == tunnel:
                if side == 'tg' or side == 'all':
                    each.tg['toggle'] = not each.tg['toggle']
                if side == 'tk' or side == 'all':
                    each.tk['toggle'] = not each.tk['toggle']

                if each.tg['toggle'] and each.tk['toggle']:
                    message += 'This TG room <===> Tk {0}'.format(each.tk['name'])
                elif each.tg['toggle'] and not each.tk['toggle']:
                    message += 'This TG room ----> Tk {0}'.format(each.tk['name'])
                elif not each.tg['toggle'] and each.tk['toggle']:
                    message += 'This TG room <---- Tk {0}'.format(each.tk['name'])
                else:
                    message += 'This TG room --x-- Tk {0}'.format(each.tk['name'])
        self.bot.sendMessage(_tgId, message)

