
class Entity(object):

    @staticmethod
    def fromDict(self, dic):
        entities = []
        for each in dic:
            entities.append(Entity(each['length'], each['type'], each['offset']))
        return entities

    def __init__(self, length, type_, offset):
        self.length = int(length)
        self.type = type_
        self.offset = int(offset)

    def fetchData(self, msg):
        return msg['text'][self.offset: self.offset + self.length]

