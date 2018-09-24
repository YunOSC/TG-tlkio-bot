
from tgbot.command import Command
from utils import *

class UnBind(Command):

    def __init__(self, cmd):
        super(UnBind, self).__init__(cmd)

    def invoke(self, msg):
        pass

    def process(self, bot, msg):
        _tgId = msg['chat']['id']
        _text = msg['text']
        tkName = _text.replace('/unbind ', '')
        if tkName == '/unbind':
            bot.sendMessage(_tgId, 'Missing TkName /unbind <TkName>')
        elif checkTunnelExists(bot.tunnels, tgId=_tgId, tkName=tkName):
            target = None
            for each in bot.tunnels:
                if each.tg['id'] == _tgId and each.tk['name'] == tkName:
                    target = each
                    break
            bot.tunnels.remove(target)
            bot.sendMessage(_tgId, 'Removed Tk[{0}]'.format(target.tk['name']))
        else:
            bot.sendMessage(_tgId, 'That TkName is not exists in binding.')
