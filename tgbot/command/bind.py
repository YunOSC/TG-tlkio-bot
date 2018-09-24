
from tgbot.command import Command
from tkbot import TkBot
from utils import *
from utils.tunnel import Tunnel

class Bind(Command):

    def __init__(self, cmd):
        super(Bind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, msg):
        _tgId = msg['chat']['id']
        _text = msg['text']
        tkName = _text.replace('/bind ', '')
        if tkName == '/bind':
            bot.sendMessage(_tgId, 'Missing TkName. /bind <TkName>')
        elif not checkTunnelExists(bot.tunnels, tgId=_tgId, tkName=tkName):
            bot.tunnels.append(Tunnel.new(_tgId, tkName))
            bot.sendMessage(_tgId, 'Binded TgId:{0} with Tk:{1}'.format(_tgId, tkName))
        else:
            bot.sendMessage(_tgId, 'That binding is already exists.')
        
