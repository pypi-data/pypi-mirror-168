#!/usr/bin/python
# -*- coding: utf-8 -*-
#  @Time    : 2021/3/24 8:57
#  @Author  : miaomiao
import random
import jsonpath
import requests,json
from aishu import setting
from aishu.public import urlJoin

class inputs(object):
    """

    """
    def createarPortId(self):
        """

        :return:
        """
        path = '/etl/input'
        url = urlJoin.url(path)
        portList = [port for port in range(20010, 20100)]
        portList.append(162)
        portList.append(514)
        portList.append(5140)
        port = random.choice(portList)
        payload = {
                "community": [],
                "port": port,
                "protocol": "tcp",
                "ruleName": "",
                "status": 1,
                "tagsID": [],
                "tags": [],
                "timezone": "Asia/Shanghai",
                "type": "ss2",
                "charset": "UTF-8"
            }

        headers = setting.header

        rsp = requests.request("POST", url, headers=headers, data = json.dumps(payload))
        m_id = jsonpath.jsonpath(rsp.json(), '$..{name}'.format(name='id'))
        if isinstance(m_id,bool):
            return False
        else:
            return m_id[0]


if __name__ == '__main__':
    date = inputs().createarPortId()
    print(date)