import argparse
import scraper


def _get_parser() -> argparse.ArgumentParser:
	"""
	Sets up required CLI parameters.
	"""
	parser = argparse.ArgumentParser(
		description='Scrape data from a Instagram profile.'
	)

	parser.add_argument(
		'url',
		help='URL of the Instagram profile to scrape.'
	)

	return parser


def main():
	parser = _get_parser()
	args = parser.parse_args()

	profile = scraper.profile(args.url)
	print(profile)


main()
