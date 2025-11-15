import configparser

config=configparser.RawConfigParser()
config.read(".\\config\\config.ini")

class Readconfig:
    @staticmethod
    def getapplicationURL():
        url=config.get('common info','baseURL')
        return url
    @staticmethod
    def getUsername():
        username=config.get('common info','username')
        return username

    @staticmethod
    def getUserpassword():
        password = config.get('common info', 'password')
        return password