import scraper


def main():
	posts = scraper.profile_recent_posts('https://www.instagram.com/nine.inch.nails/?hl=en')

	post_data = []
	for p in posts:
		post_data.append(scraper.minimise_post(p))


main()
