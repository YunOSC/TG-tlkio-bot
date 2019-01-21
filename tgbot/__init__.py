# coding=UTF-8
import traceback, threading, json, time
from threading import Event
from telebot import TeleBot

from utils import *
from tgbot.command import Command
# from tgbot.command.add_admin import AddAdmin
from tgbot.command.bind import Bind
from tgbot.command.list_bind import ListBind
from tgbot.command.toggle import Toggle
from tgbot.command.list_toggle import ListToggle
from tgbot.command.un_bind import UnBind

class TgBot(threading.Thread):

    def loadCommandConfig(self):
        pass

    def loadPersonConfig(self):
        persons = {}
        return persons

    def __init__(self, config, admins, tunnels, loopDelay=0.1, debug=False):
        super(TgBot, self).__init__()
        self.debug = debug
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.admins = admins
        self.tunnels = tunnels
        self.config = config
        self.botUserName = config['botUserName']
        self.bot = TeleBot(config['token'])
        
        self.commands = [
            # AddAdmin(bot=self, cmd=['add-admin']),
            # Alarm('alarm', time.time())
            Bind(bot=self, cmd=['b', 'bind']),
            ListBind(bot=self, cmd=['lb', 'listbind', 'list-bind']),
            Toggle(bot=self, cmd=['t', 'toggle']),
            ListToggle(bot=self, cmd=['lt', 'listtoggle', 'list-toggle']),
            UnBind(bot=self, cmd=['ub', 'unbind', 'un-bind'])
        ]
        self.persons = self.loadPersonConfig()

    def sendMessage(self, _id, _msg, parse_mode=None):
        self.bot.send_message(chat_id=_id, text=_msg, parse_mode=parse_mode)

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
                            name = _from.username or _from.first_name or _from.last_name
                            message = '[Anonymous]: {0}'.format(_text[2:]) if _text.startswith('##') else '[{0}]: {1}'.format(name, _text[1:])
                            tunnel.tk['queue'].put(message)
                if self.debug:
                    print(each)
            except Exception as e:
                if self.debug:
                    traceback.print_exc()

    def queueHandler(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.tunnels:
                tg = each.tg
                while not tg['queue'].empty() and tg['toggle']:
                    chatId = tg['id']
                    msg = tg['queue'].get()
                    try:
                        if '<img' in msg:
                            link = re.search('src=\".*?\"', msg).group(0)[5:-1]
                            if '.gif' in msg:
                                self.bot.send_document(chatId, link)
                            else:
                                self.bot.send_photo(chatId, link)
                        elif '</' in msg:
                            self.bot.send_message(chatId, msg, parse_mode='HTML')
                        else:
                            self.bot.send_message(chatId, msg, parse_mode='Markdown')
                    except Exception as e:
                        self.bot.send_message(chatId, msg)
                        if self.debug:
                            traceback.print_exc()

    def start(self):
        super(TgBot, self).start()
        for cmd in self.commands:
            cmd.register()
        self.bot.set_update_listener(self.handler)
        thread = threading.Thread(target=self.queueHandler)
        thread.start()

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            try:
                self.bot.polling(none_stop=False)
            except:
                if self.debug:
                    traceback.print_exc()

    def stop(self):
        self.bot.stop_bot()
        self.stopped.set()
