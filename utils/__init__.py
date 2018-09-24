from __future__ import unicode_literals

import requests, re

def fetchTkId(roomName):
    res = requests.get('https://tlk.io/' + roomName)
    return re.search('Talkio\.Variables\.chat_id = \'.*?\';', res.text).group(0)[28:-2]

def getMatchTunnels(tunnels, tgId=None, tkId=None, tkName=None):
    assert tgId != None or tkId != None or tkName != None
    matchTunnels = []
    for each in tunnels:
        if tgId and each.tg['id'] == tgId:
            matchTunnels.append(each)
        elif tkId and each.tk['id'] == tkId:
            matchTunnels.append(each)
        elif tkName and each.tk['name'] == tkName:
            matchTunnels.append(each)
    return matchTunnels
