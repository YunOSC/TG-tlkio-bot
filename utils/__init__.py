from __future__ import unicode_literals

from utils.user import User
import requests, re

def fetchTkId(roomName):
    res = requests.get('https://tlk.io/' + roomName)
    return re.search('Talkio\.Variables\.chat_id = \'.*?\';', res.text).group(0)[28:-2]

def checkUserExists(checkList, user):
    assert type(user) == User
    for each in checkList:
        if each == user:
            return True
    return False

def checkTunnelExists(tunnels, tgId, tkId=None, tkName=None):
    assert tkId != None or tkName != None
    for each in tunnels:
        if each.tg['id'] == tgId:
            if tkId and each.tk['id'] == tkId:
                return True
            elif tkName and each.tk['name'] == tkName:
                return True
    return False

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
