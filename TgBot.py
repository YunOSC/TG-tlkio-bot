# coding=UTF-8
import traceback, threading, json, datetime, time
from threading import Event
import telepot
from telepot.loop import MessageLoop

class TgBot(threading.Thread):

    def __init__(self, token, tgQueue, tkQueue, loopDelay=0.1):
        super(TgBot, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.toggle = False
        self.tgQueue = tgQueue
        self.tkQueue = tkQueue
        self.bot = telepot.Bot(token)
        self.roomId = None
        
    def handler(self, msg):
        try:
            _ts = msg['date']
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
            elif time.time() < _ts:
                if 'sticker' in msg:
                    sticker = msg['sticker']['file_id']
                    self.bot.sendSticker(_chat['id'], sticker)
                
        except:
            print(traceback.print_exc())

    def start(self):
        super(TgBot, self).start()
        self.duangSticker = self.bot.getStickerSet(name='DuanG')
#        print(self.duangSticker.items())

    def run(self):
        MessageLoop(self.bot, self.handler).run_as_thread()
        while not self.stopped.wait(self.loopDelay):
            if self.roomId and datetime.datetime.now().strftime('%H:%M:%S') == '06:00:00':
                time.sleep(0.5)
                self.bot.sendSticker(self.roomId, 'CAADBQADwwMAAvjGxQrfSvi6XkF9cwI') 
                self.bot.sendSticker(self.roomId, 'CAADBQADwwMAAvjGxQrfSvi6XkF9cwI') 
                self.bot.sendSticker(self.roomId, 'CAADBQADwwMAAvjGxQrfSvi6XkF9cwI') 
            while self.tgQueue.qsize() > 0 and self.toggle and self.roomId:
                self.bot.sendMessage(self.roomId, self.tgQueue.get())

    def stop(self):
        self.stopped.set()
