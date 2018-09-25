
from tgbot.command import Command
from tkbot import TkBot
from utils import *
from utils.tunnel import Tunnel

class Bind(Command):

    def __init__(self, bot, cmd):
        super(Bind, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        cmd = msg.text.split(' ')
        message = ''
        if len(cmd) > 1:
            tkName = cmd[1]
            if not checkTunnelExists(self.bot.tunnels, tgId=_tgId, tkName=tkName):
                self.bot.tunnels.append(Tunnel.new(_tgId, tkName))
                message = 'Binded TgId:{0} with Tk:{1}'.format(_tgId, tkName)
            else:
                message = 'That binding is already exists.'
        else:
            message = 'Missing TkName. /bind <TkName>'
        self.bot.sendMessage(_tgId, message)
