# coding=UTF-8
from __future__ import unicode_literals
import re, json, threading, requests, time
from threading import Event

class TkBot(threading.Thread):

    def __init__(self, tunnels, loopDelay=0.1):
        super(TkBot, self).__init__()
        self.stopped = Event()
        self.loopDelay = loopDelay

        self.tunnels = tunnels
        self.tkLink = requests.Session()

    def start(self):
        super(TkBot, self).start()
        self.tkLink.post('https://tlk.io/api/participant', data={'nickname': 'Meow3(TG)'})

    def run(self):
        while not self.stopped.wait(self.loopDelay):
            for each in self.tunnels:
                # Sending Messages
                tk = each.tk
                while not tk['queue'].empty():
                    self.tkLink.post('https://tlk.io/api/chats/{0}/messages'.format(tk['id']), data={ 'body': '\'' + tk['queue'].get() + '\'' })

                # Recieve Messages
                res = json.loads(requests.get('https://tlk.io/api/chats/{0}/messages'.format(tk['id'])).text)
                for every in res:
                    if every['timestamp'] > tk['lastTS'] and not every['deleted'] and every['nickname'] != 'Meow3(TG)':
                        message = '[{0}][{1}]: {2}'.format(tk['name'], every['nickname'], every['body'])
                        tk['lastTS'] = every['timestamp']
                        each.tg['queue'].put(message)

    def stop(self):
        self.stopped.set()
