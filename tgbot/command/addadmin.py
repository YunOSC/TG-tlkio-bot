
from tgbot.command import Command
from utils import *

class AddAdmin(Command):

    def __init__(self, bot, cmd):
        super(AddAdmin, self).__init__(bot, cmd)

    def invoke(self, msg):
        pass

    def process(self, msg):
        tgId = msg.chat.id
        from_user = User.fromSave(msg.from_user)
        if checkUserExists(self.bot.admins, from_user):
            self.bot.admins.append(from_user)
            self.bot.sendMessage(tgId, 'Added admin: {0}'.format(from_user.username))
        else:
            self.bot.sendMessage(tgId, 'You don\'t have permission to add admin.')

