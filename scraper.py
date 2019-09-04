import json
import requests
from bs4 import BeautifulSoup


def _send_request(url):
	response = requests.get(url)
	return response.text


def _extract_json(html):
	soup = BeautifulSoup(html, 'html.parser')
	body = soup.find('body')
	script_tag = body.find('script')
	raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
	return json.loads(raw_string)


def profile_recent_posts(url):
	posts = []
	response = _send_request(url)
	data = _extract_json(response)
	nodes = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']

	for n in nodes:
		node = n.get('node')
		if node and isinstance(node, dict):
			posts.append(node)

	return posts
