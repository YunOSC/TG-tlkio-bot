
from tgbot.command import Command
from tkbot import TkBot
from utils.tunnel import Tunnel

class Bind(Command):

    def __init__(self, cmd):
        super(Bind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, msg):
        _chat = msg['chat']
        _text = msg['text']
        tkName = _text.replace('/bind ', '')
        bot.tunnels.append(Tunnel.new(_chat['id'], tkName))
        bot.sendMessage(_chat['id'], 'Binded TgId:{0} with Tk:{1}'.format(_chat['id'], tkName))
        
