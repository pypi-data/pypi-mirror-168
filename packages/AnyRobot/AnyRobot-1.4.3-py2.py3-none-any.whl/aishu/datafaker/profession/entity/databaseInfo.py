from aishu import setting


class data(object):
    def getSelfDatabaseUrl(self):
        return setting.mysql_config['host']

    def getSelfDatabasePort(self):
        return setting.mysql_config['port']

    def getSelfDatabaseUser(self):
        return setting.mysql_config['user']

    def getSelfDatabasePassword(self):
        return setting.mysql_config['password']

    def getSelfDatabase(self):
        return setting.mysql_config['database']

if __name__ == '__main__':
    print(data().getSelfDatabasePort())
