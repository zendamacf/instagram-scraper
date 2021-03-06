import json
import requests
from bs4 import BeautifulSoup


class ScraperException(Exception):
	pass


def _send_request(url: str) -> requests.Response:
	"""
	Fetches HTML page from Instagram profile.
	"""
	response = requests.get(url)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError as e:
		msg = 'Got {} from {}'.format(e.response.status_code, url)
		raise ScraperException(msg) from e
	return response


def _extract_json(html: str) -> dict:
	"""
	Extracts JSON dict from HTML page string.
	"""
	soup = BeautifulSoup(html, 'html.parser')
	body = soup.find('body')
	script = body.find('script').text.strip()
	raw_string = script.replace('window._sharedData =', '').replace(';', '')
	return json.loads(raw_string)


def _minimise_post(post: dict) -> dict:
	"""
	Simplifies post JSON dict into only relevant information.
	"""
	min_post = {
		'id': post['id'],
		'post_url': 'https://www.instagram.com/p/{}/'.format(post['shortcode']),
		'image_url': None,
		'caption': post['edge_media_to_caption']['edges'][0]['node']['text'],
	}

	max_width = 0
	# Find the largest thumbnail
	for thumbnail in post['thumbnail_resources']:
		if thumbnail['config_width'] > max_width:
			min_post['image_url'] = thumbnail['src']
			max_width = thumbnail['config_width']

	return min_post


def _profile_recent_posts(user: dict) -> list:
	"""
	Gets recent posts from a Instagram JSON dict.
	"""
	posts = []
	nodes = user['edge_owner_to_timeline_media']['edges']

	for n in nodes:
		node = n.get('node')
		if node and isinstance(node, dict):
			posts.append(_minimise_post(node))

	return posts


def _minimise_profile(user: dict) -> dict:
	"""
	Simplifies profile JSON dict into only relevant information.
	"""
	profile_data = {
		'id': user['id'],
		'username': user['username'],
		'full_name': user['full_name'],
		'biography': user['biography'],
		'profile_url': 'https://www.instagram.com/{}/'.format(user['username']),
		'image_url': user['profile_pic_url_hd'],
		'follower_count': user['edge_followed_by']['count'],
		'follow_count': user['edge_follow']['count'],
		'post_count': user['edge_owner_to_timeline_media']['count'],
		'recent_posts': _profile_recent_posts(user)
	}
	return profile_data


def _parse_user(json_data: dict) -> dict:
	return json_data['entry_data']['ProfilePage'][0]['graphql']['user']


def profile(url: str) -> dict:
	"""
	Fetches profile data for a given Instagram URL.
	"""
	response = _send_request(url).text
	json_data = _extract_json(response)

	user = _parse_user(json_data)
	profile_data = _minimise_profile(user)

	return profile_data
