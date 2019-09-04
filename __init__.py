import scraper


def main():
	posts = scraper.profile_recent_posts('https://www.instagram.com/nine.inch.nails/?hl=en')

	for p in posts:
		print(p)
		print()
		print()


main()
