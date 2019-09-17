import json
import scraper
from .helpers import load_file


def test_send_request():
	resp = scraper._send_request('https://www.github.com/')
	assert(resp.status_code == 200)


def test_send_request_fail():
	try:
		scraper._send_request('https://www.github.com/404')
		assert(False)
	except scraper.ScraperException:
		assert(True)


def test_extract_json():
	html = load_file('resources/profile.html')
	extracted = scraper._extract_json(html)
	json_data = json.loads(load_file('resources/profile.json'))
	assert(extracted == json_data)


def test_minimise_profile():
	json_data = json.loads(load_file('resources/profile.json'))
	user = scraper._parse_user(json_data)
	profile = scraper._minimise_profile(user)
	assert(profile['full_name'] == 'GitHub')


def test_profile_recent_posts():
	json_data = json.loads(load_file('resources/profile.json'))
	user = scraper._parse_user(json_data)
	posts = scraper._profile_recent_posts(user)
	assert(posts[0]['id'] == '2061107916421637466')
