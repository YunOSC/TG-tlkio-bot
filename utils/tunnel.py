from __future__ import unicode_literals

from utils import *
import Queue, time

class Tunnel(object):

    @staticmethod
    def fromSave(dic):
        return Tunnel(dic['tg'], dic['tk'])

    @staticmethod
    def new(tgId, tkName):
        tg = {
            'id': tgId,
            'toggle': False
        }
        tk = {
            'id': fetchTkId(tkName),
            'name': tkName, 
            'toggle': False,
            'lastTS': time.time()
        }
        return Tunnel(tg, tk)

    def __init__(self, tg, tk):
        self.tg = {
            'id': tg['id'],
            'toggle': tg['toggle'],
            'queue': Queue.Queue()
        }
        self.tk = {
            'id': tk['id'],
            'name': tk['name'],
            'toggle': tk['toggle'],
            'queue': Queue.Queue(),
            'lastTS': tk['lastTS']
        }

    def toSave(self):
        return {
            'tg': {
                'id': self.tg['id'],
                'toggle': self.tg['toggle']
            },
            'tk': {
                'id': self.tk['id'],
                'name': self.tk['name'],
                'toggle': self.tk['toggle'],
                'lastTS': self.tk['lastTS']
            }
        }

