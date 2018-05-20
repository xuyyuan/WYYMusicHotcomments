import requests
from requests.exceptions import RequestException
import json
import pymongo

client = pymongo.MongoClient('localhost')
db = client['douban']

def get_data():
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_254574?csrf_token='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
    }
    params = 'DKFuoRPLMtNX4KiF6SSwS8NJg7juv/RNPjBOJuYqBfxUStwo9TXLhiVAkJbYA8ULk9B/3KbPRGXSpJRzAXQJzlTemHqHu8Q+xvh5/l4XG4r5KpZiaO7DAB+PCJ5XdUR8SiCHrWvd0vJKrs4xqG5GMeZVu7UdcRW03w0Y3pl8S+kX+V2acjjFVtzLmwI7jpRe'
    encSecKey = '9dda05a032f09d90ff45211e127b42192735ee09cda8a54f25b73b0d674de10f4d09d63c05ed7d3dd85752bf1eac2422b9d1fa9afb6e07235f3ecba149245b7be8a3e94819086d865999aecb8e560e873b3a27ad9c7153ac03c8b0f309f98cceb38f55dd3daa4c6f763fea3ed28edbf2f374052dc3af883d01c56f02e88829b6'
    data = {
        'params':params,
        'encSecKey':encSecKey,
    }
    try:
        res = requests.post(url, headers=headers, data=data)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_data(data):
    data = json.loads(data)
    if 'hotComments' in data.keys( ):
        for each in data.get('hotComments'):
            # yield  {
            #     'nickname': each.get('user').get('nickname'),
            #     'content':each.get('content'),
            # }
            # 以上是 字典的形式用于存储到monodb中
            yield [each.get('user').get('nickname'), each.get('content')]  # 这里采用常用的列表形式

def save_to_mongodb(content):
    try:
        if db['music'].insert(content):
            print('存储到mongodb成功！', content)
    except Exception:
        print('存储到mongodb失败！', content)

def save_to_file(content):
    with open(r'comment.txt', 'a', encoding='utf-8') as file: # 注意是'a'的形式，下边的的代码决定了每次都要打开文件进行写入
        file.write(content[0] + '\n')
        file.write(content[1] + '\n')
        file.write('--------------------------------------------'+'\n')
        # 如果存储到文件的话，spider2的存储方式会比较好些

def main():
    data = get_data()
    for item in parse_data(data):
        save_to_file(item)
        # save_to_mongodb(item)

if __name__ == '__main__':
    main()