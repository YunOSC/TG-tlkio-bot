
from utils import *
from tgbot.command import Command

class Toggle(Command):

    def __init__(self, bot, cmd):
        super(Toggle, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        _tgId = msg.chat.id
        for each in getMatchTunnels(self.bot.tunnels, tgId=_tgId):
            each.tg['toggle'] = not each.tg['toggle']
        self.bot.sendMessage(_tgId, 'Toggled')

