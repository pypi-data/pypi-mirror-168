from aishu.datafaker.anyrobot.getSqlVaule import AnyRobotDataServer
from aishu.datafaker.profession.getFiledValue import filed
from aishu import setting

class faker():
    def __init__(self,testEnv_config,mysql_config):
        self.testEnv_config = testEnv_config
        self.mysql_config =  mysql_config

        #获取测试环境数据库信息
        setting.mysql_config['host'] = self.mysql_config['host']
        setting.mysql_config['port'] = self.mysql_config['port']
        setting.mysql_config['user'] = self.mysql_config['user']
        setting.mysql_config['password'] = self.mysql_config['password']
        setting.mysql_config['database'] = self.mysql_config['database']

        #获取测试环境url信息
        setting.testEnv_config['ip'] = self.testEnv_config['ip']
        setting.testEnv_config['protocol'] = self.testEnv_config['protocol']
        setting.testEnv_config['port'] = self.testEnv_config['port']

    def route(self,key,result=[]):
        date = AnyRobotDataServer(key).getValue()
        if isinstance(date, bool):
            date = filed(key, result)
            return date
        else:
            return date

if __name__ == '__main__':
    mysql_config = {
        'host': '',
        'port': 3306,
        'user': '',
        'password': '',
        'database': ''

    }
    testEnv_config = {
        'ip': '',
        'protocol': 'http',
        'port': '80'
    }
    key=''
    date1 = faker(testEnv_config,mysql_config).route(key)
    print(date1)