from __future__ import unicode_literals
import sys, json, Queue

from tgbot import TgBot
from TkBot import TkBot

tkRoomId = 8099831

def loadConfig(path):
    with open(path) as f:
        config = json.loads(f.read())
    return config

def writeConfig(config, path):
    try:
        data = json.dumps(config, indent=4)
        with open(path, 'w'): pass # Clear file content
        with open(path, 'w') as f:
            f.write(data)
    except:
        pass

if __name__ == "__main__":
    path = './config.json'
    config = loadConfig(path)
    tgQueue = Queue.Queue()
    tkQueue = Queue.Queue()
    tgBot = TgBot(config['telegramBot'], tgQueue=tgQueue, tkQueue=tkQueue)
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
#                writeConfig(config)
                sys.exit(0)
        except KeyboardInterrupt:
            tgBot.stop()
            tkBot.stop()
            sys.exit(0)
        

