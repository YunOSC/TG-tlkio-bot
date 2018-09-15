# coding=UTF-8
import traceback, threading, json
from threading import Event
import telepot
from telepot.loop import MessageLoop

from Pair import Pair

class TgBot(threading.Thread):

    def __init__(self, config, tgQueue, tkQueue, loopDelay=0.1):
        super(TgBot, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.toggle = False
        self.tgQueue = tgQueue
        self.tkQueue = tkQueue
        self.config = config
        self.botUserName = config['telegramBot']['botUserName']
        self.bot = telepot.Bot(config['telegramBot']['token'])
        self.roomId = None
        
        self.groups = config['telegramGroupId']
        self.pairs = Pair.fromJson(config['pair'])

    def handler(self, msg):
        try:
            _from = msg['from']
            _chatId = msg['chat']['id']
            if 'left_chat_participant' in msg and 'username' in msg['left_chat_participant']:
                leftUserName = msg['left_chat_participant']['username']
                if leftUserName == self.botUserName and _chatId in self.groups:
                    self.groups.remove(_chatId)
                    print('{0} has removed from groups list.'.format(_chatId))
            elif 'new_chat_participant' in msg and 'username' in msg['new_chat_participant']:
                addUserName = msg['new_chat_participant']['username']
                if addUserName == self.botUserName and not _chatId in self.groups:
                    self.groups.append(_chatId)
                    print('{0} has added into groups list.'.format(_chatId))
            else:
                _text = msg['text']
                if _text.startswith('/status'):
                    self.bot.sendMessage(_chatId, json.dumps(Pair.toJson(self.pairs), indent=4))
                elif _text.startswith('/pair '):
                    tlkId = _text.replace('/pair ', '')
                    if tlkId in self.pairs:
                        self.pairs[tlkId].tgGroupsID.append(_chatId)
                        self.bot.sendMessage(_chatId, 'This group is appended into id {0}\'s list.'.format(tlkId))
                    else:
                        self.pairs[tlkId] = Pair(tlkId, False, [_chatId])
                        self.bot.sendMessage(_chatId, 'id {0} is not exists yet, create one.'.format(tlkId))
                elif _text.startswith('/unpair '):
                    tlkId = _text.replace('/unpair ', '')
                    if not tlkId in self.pairs:
                        self.bot.sendMessage(_chatId, 'id {0} is not in pairs list'.format(tlkId))
                    elif not _chatId in self.pairs[tlkId].tgGroupsID:
                        self.bot.sendMessage(_chatId, 'This group is not in id {0}\'s pair groups'.format(tlkId))
                    else:
                        self.pairs[tlkId].tgGroupsID.remove(_chatId)
                        if len(self.pairs[tlkId].tgGroupsID) == 0:
                            self.bot.sendMessage(_chatId, 'id {0}\'s pair group is empty, remove from list'.format(tlkId))
                            del self.pairs[tlkId]
                        else:
                            self.bot.sendMessage(_chatId, 'This telegram group is removed from id {0}\'s groups list'.format(tlkId))
                elif _text.startswith('/toggle'):
                    tlkId = _text.replace('/toggle ', '')
                    if tlkId:
                        if tlkId in self.pairs:
                            self.pairs[tlkId].toggle = not self.pairs[tlkId].toggle
                            self.bot.sendMessage(_chatId, 'id {0}\' mode has been toggle to {1}'.format(tlkId, self.pairs[tlkId].toggle))
                        else:
                            self.bot.sendMessage(_chatId, 'This id is not exists in list')
                    else:
                        for (key, value) in self.pairs.items():
                            if _chatId in value.tgGroupsId:
                                value.toggle = not value.toggle
                                self.bot.sendMessage(_chatId, 'id {0}\'s mode has been toggle to {1} '.format(key, value.toggle))
            
            print(msg)
            _text = msg['text'] if 'text' in msg else ''
            _chat = msg['chat']
            _from = msg['from']
            if _text.startswith('/course'):
                if _from['username'] != 'Clo5de':
                    self.bot.sendMessage(_chat['id'], '@{0} 你他媽是智障= =？ 試三小拉幹你老師'.format(_from['username']))
                    print('{0} just try to open course mode'.format(_from['username']))
                else:
                    self.toggle = not self.toggle
                    self.bot.sendMessage(_chat['id'], 'Course mode set to {0} by {1}'.format(self.toggle, _from['username']))
                    self.roomId = _chat['id']
                    print('{0} has toggle course mode to {1} at roomId {2}'.format(_from['username'], self.toggle, self.roomId))
            elif _text.startswith('##') and self.toggle:
                message = '[Anonymous]: {0}'.format(_text[2:].encode('utf-8'))
                self.tkQueue.put(message)
            elif _text.startswith('#') and self.toggle:
                message = '[{0}]: {1}'.format(_from['username'], _text[1:].encode('utf-8'))
                self.tkQueue.put(message)
        except:
            print(traceback.print_exc())

    def start(self):
        super(TgBot, self).start()

    def run(self):
        MessageLoop(self.bot, self.handler).run_as_thread()
        while not self.stopped.wait(self.loopDelay):
            while self.tgQueue.qsize() > 0 and self.toggle and self.roomId:
                self.bot.sendMessage(self.roomId, self.tgQueue.get())

    def stop(self):
        self.stopped.set()
        self.config['pair'] = Pair.toJson(self.pairs)
