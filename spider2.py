import requests
import json

def get_one_page(url):
    data_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(url.split('=')[-1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Referer':'http://music.163.com/song?id=475277345'
    }
    params = '7/keSqS9RvKsWdeVlPt76ahXvFxh0fZHHVyei8lkrcBx4vWdNA/i1IL8MZ5uLHhd0cdu5dJOUs1POBSNJgsnnXU8/vh+HL9B0kjLoTUZgODKo1xbhBLX+GYG8XmvKxmfBjFn7PihPX5sLGFGu0ioy4OXYpJeyXJb3mO+b/IMuEJODShfoUexvii4MMpvYQhb'
    encSecKey = 'dbb05589bdd4ac642b135eb01840de3b98a024162fda1b6a1ec12e518d3afc4f1d6c239294f92b696a15a38c7c53aca87040a700bf12952af8754680ca2f11471016f9ab739474d2268aec1f6272185ecf9153ef19a98f1ff81b092e64a1a496abea5cb0508b715cfac111489d8e9278ae067258661b1e276c10183a4f143292'
    data = {
        'params': params,
        'encSecKey':encSecKey
    }
    res = requests.post(data_url, headers=headers, data=data)
    return res.text

def parse_one_page(html):
    data = json.loads(html)
    if 'hotComments' in data.keys():   # 处理json字符串
        for each in data.get('hotComments'):
            yield [
                each.get('user').get('nickname'),
                each.get('content')
            ]

def main():
    url = input('请输入歌曲所在的网址：')
    html = get_one_page(url)
    with open(r'hotcomments.txt', 'w', encoding='utf-8') as file:
        for each in parse_one_page(html):
            file.write(each[0] + '\n')
            file.write(each[1] + '\n')
            file.write('-----------------------------------\n')

if __name__ == '__main__':
    main()