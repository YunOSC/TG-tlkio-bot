
class User(object):

    @staticmethod
    def fromSave(config):
        firstName = config['first_name']
        lastName = config['last_name']
        userName = config['username']
        return User(firstName, lastName, userName)

    def __init__(self, firstName, lastName, userName):
        assert firstName or lastName or userName
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName

    def __eq__(self, that):
        assert type(that) == dict
        rtn = self.firstName and that['first_name'] == self.firstName
        rtn = self.lastName and that['last_name'] == self.lastName
        rtn = self.userName and that['username'] == self.userName
        return rtn

    def toSave(self):
        return {
            'first_name': self.firstName,
            'last_name': self.lastName,
            'username': self.userName
        }

