from __future__ import unicode_literals
import click
import traceback, sys, json
if sys.version[0] == '3':
    raw_input = input

from tgbot import TgBot
from tkbot import TkBot
from utils.user import User
from utils.tunnel import Tunnel

def loadConfig(path):
    with open(path) as f:
        config = json.loads(f.read())
    return config

def loadAdmin(config):
    configList = config['admin']
    admins = []
    for each in configList:
        admins.append(User.fromSave(each))
    return admins

def loadBind(config):
    configList = config['bindTgTk']
    tunnels = []
    for each in configList:
        tunnels.append(Tunnel.fromSave(each))
    return tunnels

def writeAdmin(config, admins):
    config['admin'] = []
    for each in admins:
        config['admin'].append(each.toSave())

def writeBind(config, tunnels):
    config['bindTgTk'] = []
    for each in tunnels:
        config['bindTgTk'].append(each.toSave())

def writeConfig(config, admins, tunnels, path):
    writeAdmin(config, admins)
    writeBind(config, tunnels)
    data = json.dumps(config, indent=4)
    with open(path, 'w'): pass # Clear file content
    with open(path, 'w') as f:
        f.write(data)

@click.command()
@click.option('--start', default=False, type=bool)
@click.option('--path', default='./config.json', type=str)
@click.option('--debug', default=False, type=bool)
def run(start, path, debug):
    config = loadConfig(path)
    admins = loadAdmin(config)
    tunnels = loadBind(config)
    tgBot = TgBot(config=config['telegramBot'], admins=admins, tunnels=tunnels, debug=debug)
    tkBot = TkBot(admins=admins, tunnels=tunnels, debug=debug)

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
                writeConfig(config=config, admins=admins, tunnels=tunnels, path=path)
                sys.exit(0)
        except KeyboardInterrupt:
            tgBot.stop()
            tkBot.stop()
            sys.exit(0)
        except Exception as e:
            if debug:
                traceback.print_exc()
    

if __name__ == "__main__":
    run()

