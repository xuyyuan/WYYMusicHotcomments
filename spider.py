import requests
import json

def get_comments(url):
	name_id = url.split('=')[1]
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
	'Referer': 'http://music.163.com/song?id=4466775'}
	params = 'AGWpZBXccksJCyXyh/PCPkW7myAiZWaOUDlpMx18XpsQQ4URHgphCtEWm9S64nhNhE0BAvsDgwbJhJQFT5xKCJTrvol15f80HLCd6bmRYuoAQntLbvHprZcGUmh/w67sU0fbWYXo3i4VQmPh2tMH1OA3MsFolp9HyQ0liVEMpLJ40OrMfKWHog623JF5L2aq'
	encSecKey = '47e580a4717d651fe44947ba3b8e27751fc172bb7687cc5a37dd1f3cdd5f228d8f8b2c9f3be560eff043cf75107a9bb447ef22b4f2a7ff1fec6532a73d728f7d04d25dd9eb0bbac8646ee00485165e360c0875ac6142ab8d842b2641d361d6ed95a429e525c74b490e4420e259536acc6c6f9fdd15290eefdc0917ec5afc8cf9'
	data = {'params':params, 'encSecKey':encSecKey}
	target_url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(name_id)
	res = requests.post(target_url, headers=headers, data=data)
	return res

def get_hot_comments(res):
	comments_json = json.loads(res.text)
	hot_comments = comments_json['hotComments']
	with open('Hotcomments.txt', 'w', encoding='utf-8') as f:
		for each in hot_comments:
			f.write(each['user']['nickname'] + '\n\n')
			f.write(each['content'] + '\n')
			f.write('------------------------------------------\n')

def main():
	url = input('请输入链接地址：')
	res = get_comments(url)
	get_hot_comments(res)

if __name__ == '__main__':
	main()
