
from utils import *
from tgbot.command import Command

class Toggle(Command):

    def __init__(self, cmd):
        super(Toggle, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, cmd, msg):
        _tgId = msg['chat']['id']
        for each in getMatchTunnels(bot.tunnels, tgId=_tgId):
            each.tg['toggle'] = not each.tg['toggle']
        bot.sendMessage(_tgId, 'Toggled')

