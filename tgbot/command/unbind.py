
from tgbot.command import Command
from utils import *

class UnBind(Command):

    def __init__(self, bot, cmd):
        super(UnBind, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        cmd = msg.text.split(' ')
        if len(cmd) > 1:
            tkName = cmd[1]
            if tkName == 'global':
                self.bot.tunnels.clear()
                self.bot.sendMessage(_tgId, 'All tunnels are cleared.')
            elif checkTunnelExists(self.bot.tunnels, tgId=_tgId, tkName=tkName):
                target = None
                for each in self.bot.tunnels:
                    if each.tg['id'] == _tgId and each.tk['name'] == tkName:
                        target = each
                        break
                self.bot.tunnels.remove(target)
                self.bot.sendMessage(_tgId, 'Removed Tk[{0}]'.format(target.tk['name']))
            else:
                self.bot.sendMessage(_tgId, 'That TkName is not exists in binding.')
        else:
            self.bot.sendMessage(_tgId, 'Missing TkName /unbind <TkName>')
