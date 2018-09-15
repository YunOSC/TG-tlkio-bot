from __future__ import unicode_literals
import sys, json, Queue

from TgBot import TgBot
from TkBot import TkBot

tgToken= '652483905:AAEPmruMxQAvI0weh2zL4R8-_VY6QwYYxJ0'
tkRoomId = 8099831

if __name__ == "__main__":
    tgQueue = Queue.Queue()
    tkQueue = Queue.Queue()
    tgBot = TgBot(tgToken, tgQueue=tgQueue, tkQueue=tkQueue)
    tkBot = TkBot(tkRoomId, tkQueue=tkQueue, tgQueue=tgQueue)

    while True:
        try:
            userInput = raw_input('> ')
            if 'start' in userInput:
                tgBot.start()
                tkBot.start()
            elif 'stop' in userInput:
                tgBot.stop()
                tkBot.stop()
                sys.exit(0)
        except KeyboardInterrupt:
            tgBot.stop()
            tkBot.stop()
            sys.exit(0)
        

