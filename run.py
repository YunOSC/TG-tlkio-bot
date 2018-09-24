from __future__ import unicode_literals
import click
import sys, json
if sys.version[0] == '3':
    raw_input = input

from tgbot import TgBot
from tkbot import TkBot
from utils.tunnel import Tunnel

tkRoomId = 8099831

def loadConfig(path):
    with open(path) as f:
        config = json.loads(f.read())
    return config

def loadBind(config):
    bindList = config['bindTgTk']
    tunnelList = []
    for each in bindList:
        tunnelList.append(Tunnel.fromSave(each))
    return tunnelList

def writeBind(config, tunnels):
    config['bindTgTk'] = []
    for each in tunnels:
        config['bindTgTk'].append(each.toSave())
        

def writeConfig(config, tunnels, path):
    try:
        writeBind(config, tunnels)
        data = json.dumps(config, indent=4)
        with open(path, 'w'): pass # Clear file content
        with open(path, 'w') as f:
            f.write(data)
    except:
        pass

@click.command()
@click.option('--start', default=False, type=bool)
def run(start):
    path = './config.json'
    config = loadConfig(path)
    tunnels = loadBind(config)
    tgBot = TgBot(config['telegramBot'], tunnels=tunnels)
    tkBot = TkBot(tunnels=tunnels)

    if start:
        tgBot.start()
        tkBot.start()

    while True:
        try:
            userInput = raw_input('> ')
            if 'start' in userInput:
                tgBot.start()
                tkBot.start()
            elif 'stop' in userInput:
                tgBot.stop()
                tkBot.stop()
                writeConfig(config, tunnels, path)
                sys.exit(0)
        except KeyboardInterrupt:
            tgBot.stop()
            tkBot.stop()
            sys.exit(0)

if __name__ == "__main__":
    run()

