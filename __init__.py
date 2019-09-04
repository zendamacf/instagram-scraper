import scraper


def _parse_post_data(post):
	post_data = {
		'post_url': 'https://www.instagram.com/p/{}/'.format(post['shortcode']),
		'image_url': None,
		'caption': post['edge_media_to_caption']['edges'][0]['node']['text'],
	}

	max_width = 0
	# Find the largest thumbnail
	for thumbnail in post['thumbnail_resources']:
		if thumbnail['config_width'] > max_width:
			post_data['image_url'] = thumbnail['src']
			max_width = thumbnail['config_width']

	return post_data


def main():
	posts = scraper.profile_recent_posts('https://www.instagram.com/nine.inch.nails/?hl=en')

	post_data = []
	for p in posts:
		post_data.append(_parse_post_data(p))

main()
