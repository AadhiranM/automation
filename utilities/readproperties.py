import configparser

config=configparser.RawConfigParser()
config.read(".\\config\\config.ini")

class Readconfig:
    @staticmethod
    def getAccessCode():
        access_code = config.get('common info', 'access_code')
        return access_code

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

