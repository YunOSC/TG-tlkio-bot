from __future__ import unicode_literals
import sys, json, Queue

from TgBot import TgBot
from TkBot import TkBot

tkRoomId = 8099831

def loadConfig(default='./config.json'):
    with open(default) as f:
        config = json.loads(f.read())
    return config

def writeConfig(config, default='./config.json'):
    try:
        data = json.dumps(config, indent=4)
        with open(default, 'w'): pass # Clear file content
        with open(default, 'w') as f:
            f.write(data)
    except:
        pass

if __name__ == "__main__":
    config = loadConfig()
    tgQueue = Queue.Queue()
    tkQueue = Queue.Queue()
    tgBot = TgBot(config, tgQueue=tgQueue, tkQueue=tkQueue)
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
                writeConfig(config)
                sys.exit(0)
        except KeyboardInterrupt:
            tgBot.stop()
            tkBot.stop()
            sys.exit(0)
        

