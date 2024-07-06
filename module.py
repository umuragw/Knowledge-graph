import requests
import re
import json
import pandas as pd
def run_spider(url):
    l1 = []
    l2 = []
    # url = "http://www.ngac.org.cn/datacenter/national/find"

    for page in range(1, 14):
        payload = "{\"page\":1,\"limit\":10,\"queryAll\":\"四川省地质灾害\",\"fq\":false}"
        # 将 JSON 字符串解析为 Python 字典
        data = json.loads(payload)

        # 修改特定字段的值
        data["page"] = page

        # 将修改后的 Python 字典转换回 JSON 字符串
        payload = json.dumps(data)

        # 将 payload 编码为 UTF-8
        payload_encoded = payload.encode('utf-8')

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'Hm_lvt_0fa74f421564fdb28aabc791770ab182=1709741815; Hm_lpvt_0fa74f421564fdb28aabc791770ab182=1709741815',
            'Origin': 'http://www.ngac.org.cn',
            'Referer': 'http://www.ngac.org.cn/datacenter/national?fq=false&q=%E5%9B%9B%E5%B7%9D%E7%9C%81%E5%9C%B0%E8%B4%A8%E7%81%BE%E5%AE%B3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.post(url, headers=headers, data=payload_encoded)
        # response.text

        # 使用正则表达式提取 mdIdnt 后面的 mdIdnt 号
        ids = re.findall(r'"mdIdnt":"(.*?)"', response.text)

        for inner_id in ids:
            inner_url = "http://www.ngac.org.cn/ngac-server/rest/data/fileList/1"

            payload = "{\"mdidnt\":\"cgdoi.n0001/x00145567\",\"MetaId\":\"\"}"
            # 将 JSON 字符串解析为 Python 字典
            data = json.loads(payload)

            # 修改特定字段的值
            data["mdidnt"] = inner_id

            # 将修改后的 Python 字典转换回 JSON 字符串
            payload = json.dumps(data)
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': 'Hm_lvt_0fa74f421564fdb28aabc791770ab182=1709741815; Hm_lpvt_0fa74f421564fdb28aabc791770ab182=1709747738',
                'Origin': 'http://www.ngac.org.cn',
                'Referer': 'http://www.ngac.org.cn/Data/archivesDetails?mdidnt=cgdoi.n0001%2Fx00143575',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'is_ajax_request': 'true'
            }

            response = requests.request("POST", inner_url, headers=headers, data=payload)

            ids = re.findall(r'"abs":"(.*?)"', response.text)
            l2.append(ids[0].replace('\\n', '').replace('\\r', ''))

            response = response.json()
            title = response["body"]["dataSet"]["dataMeta"]["dataVisitor"]

            l1.append(title[0]['title'])
    # 创建一个字典，其中键是列名，值是数据列表
    data = {'标题': l1, '内容': l2}

    # 将字典转换为DataFrame
    df = pd.DataFrame(data)
    return df
