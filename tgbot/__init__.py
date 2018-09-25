# coding=UTF-8
import traceback, threading, json, time
from threading import Event
from telebot import TeleBot

from utils import *
from tgbot.command import Command
from tgbot.command.bind import Bind
from tgbot.command.listbind import ListBind
from tgbot.command.toggle import Toggle
from tgbot.command.unbind import UnBind

class TgBot(threading.Thread):

    def loadCommandConfig(self):
        pass

    def loadPersonConfig(self):
        persons = {}
        return persons

    def __init__(self, config, tunnels, loopDelay=0.1):
        super(TgBot, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.tunnels = tunnels
        self.config = config
        self.botUserName = config['botUserName']
        self.bot = TeleBot(config['token'])
        
        self.commands = [
            #Alarm('alarm', time.time())
            Bind(bot=self, cmd=['b', 'bind']),
            ListBind(bot=self, cmd=['lb', 'listbind']),
            Toggle(bot=self, cmd=['t', 'toggle']),
            UnBind(bot=self, cmd=['ub', 'unbind'])
        ]
        self.persons = self.loadPersonConfig()

    def sendMessage(self, _id, _msg):
        self.bot.send_message(_id, _msg)

    def replyTo(self, msg, _msg):
        self.bot.reply_to(msg, _msg)

    def listbind_handler(self, message):
        print(message)

    def handler(self, msg):
        for each in msg:
            try:
                _from = each.from_user
                _chat = each.chat
                if each.text and each.text.startswith('#'):
                    _text = each.text
                    for tunnel in getMatchTunnels(self.tunnels, tgId=_chat.id):
                        if tunnel.tg['toggle']:
                            message = '[Anonymous]: {0}'.format(_text[2:]) if _text.startswith('##') else '[{0}]: {1}'.format(_from.username, _text[1:])
                            tunnel.tk['queue'].put(message)
            except:
                print(traceback.print_exc())

    def queueHandler(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.tunnels:
                tg = each.tg
                while not tg['queue'].empty() and tg['toggle']:
                    self.sendMessage(tg['id'], tg['queue'].get())

    def start(self):
        super(TgBot, self).start()

    def run(self):
        for cmd in self.commands:
            cmd.register()
        self.bot.set_update_listener(self.handler)
        thread = threading.Thread(target=self.queueHandler)
        thread.start()
        self.bot.polling()

    def stop(self):
        self.bot.stop_bot()
        self.stopped.set()
