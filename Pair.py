# coding=UTF-8
import json

class Pair(object):

    def __init__(self, tlkID, toggle, tgGroupsID):
        self.tlkID = tlkID
        self.toggle = toggle
        self.tgGroupsID = tgGroupsID

    def toDict(self):
        return { "toggle": self.toggle, "tgGroups": self.tgGroupsID }

    @staticmethod
    def fromJson(config):
        pairs = {}
        for (key, value) in config.items():
            pairs[key] = Pair(key, value['toggle'], value['tgGroups'])
        if len(pairs.keys()) == 0:
            print('You don\'t have any paris!')
        return pairs

    @staticmethod
    def toJson(config):
        pairs = {}
        for (key, value) in config.items():
            pairs[key] = value.toDict()
        return pairs

