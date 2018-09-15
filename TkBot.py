# coding=UTF-8
import json, threading, requests, time
from threading import Event

class TkBot(threading.Thread):

    def __init__(self, roomId, tkQueue, tgQueue, loopDelay=0.1):
        super(TkBot, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.tkQueue = tkQueue
        self.tgQueue = tgQueue
        self.roomId = roomId
        self.lastTS = time.time()
        self.tkLink = requests.Session()

    def start(self):
        super(TkBot, self).start()
        self.tkLink.post('https://tlk.io/api/participant', data={'nickname': 'Meow3(TG)'})

    def run(self):
        self.tkLink.post('https://tlk.io/api/chats/{0}/messages'.format(self.roomId), data={'body': 'Bot is Online! You MotherFxxckers!!!'})
        while not self.stopped.wait(self.loopDelay):
            while self.tkQueue.qsize() > 0:
                msg = self.tkQueue.get()
                res = self.tkLink.post('https://tlk.io/api/chats/{0}/messages'.format(self.roomId), data={ 'body': '\'' + msg + '\'' })

            res = json.loads(requests.get('https://tlk.io/api/chats/{0}/messages'.format(self.roomId)).text)
            if res == []:
                continue
            else:
                for each in res:
                    if each['timestamp'] <= self.lastTS:
                        pass
                    elif not each['deleted'] and each['nickname'] != 'Meow3(TG)':
                        message = '[{0}]: {1}'.format(each['nickname'], each['body'].encode('utf-8'))
                        self.lastTS = each['timestamp']
                        self.tgQueue.put(message)

    def stop(self):
        self.stopped.set()
