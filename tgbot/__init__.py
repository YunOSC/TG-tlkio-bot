# coding=UTF-8
import traceback, threading, json, time
from threading import Event
import telepot
from telepot.loop import MessageLoop

from utils import *
from tgbot.command import Command
from tgbot.command.bind import Bind
from tgbot.command.listbind import ListBind
from tgbot.command.toggle import Toggle

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

        self.toggle = False
        self.tunnels = tunnels
        self.config = config
        self.botUserName = config['botUserName']
        self.bot = telepot.Bot(config['token'])
        self.roomId = None
        
        self.commands = [
            #Alarm('alarm', time.time())
            Bind('bind'),
            ListBind('listbind'),
            Toggle('toggle')
        ]
        self.persons = self.loadPersonConfig()

    def sendMessage(self, _id, _msg):
        self.bot.sendMessage(_id, _msg)


    def handler(self, msg):
        try:
            _from = msg['from']
            _chat = msg['chat']
            if msg['text'].startswith('/'):
                for each in self.commands:
                    if msg['text'].startswith('/' + each.cmd): #msg['text'].startswith('/' + type(each).__name__.lower()):
                        return each.process(self, msg)
                self.sendMessage(_chat['id'], 'Unknown command')
            else:
                _text = msg['text']
                for tunnel in getMatchTunnels(self.tunnels, tgId=_chat['id']):
                    if tunnel.tg['toggle'] and _text.startswith('#'):
                        if _text.startswith('##'):
                            message = '[Anonymous]: {0}'.format(_text[2:])
                        else:
                            message = '[{0}]: {1}'.format(_from['username'], _text[1:])
                        tunnel.tk['queue'].put(message)
            
        except:
            print(traceback.print_exc())
        finally:
            return 

    def start(self):
        super(TgBot, self).start()

    def run(self):
        MessageLoop(self.bot, self.handler).run_as_thread()
        while not self.stopped.wait(self.loopDelay):
            for each in self.tunnels:
                tg = each.tg
                while not tg['queue'].empty() and tg['toggle']:
                    self.bot.sendMessage(tg['id'], tg['queue'].get())

    def stop(self):
        self.stopped.set()
