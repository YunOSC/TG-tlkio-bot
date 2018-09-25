
from telebot import TeleBot

class Command(object):

    def __init__(self, bot, cmd, invoke=False, **kwargs):
        assert type(cmd) == list
        self.bot = bot
        self.cmd = cmd
        self.invoke = invoke
        for (key, value) in kwargs.items():
            setattr(key, value)

    def register(self):
        self.bot.bot.add_message_handler(TeleBot._build_handler_dict(self.process, commands=self.cmd))

    def invoke(self, msg):
        raise NotImplementedError

    def process(self, bot, cmd, **kwargs):
        raise NotImplementedError


