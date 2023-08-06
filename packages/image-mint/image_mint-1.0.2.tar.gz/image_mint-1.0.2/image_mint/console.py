"""
Used for running in the terminal
"""
import os
import argparse
import image_mint.engines as engines
from image_mint import Scraper


def main():
    parser = argparse.ArgumentParser(
        description="Scrape images from the internet.")
    parser.add_argument("search", help="Search keywords")
    parser.add_argument("-e", "--engine", required=False, default="Google", choices=['Google', 'Bing', 'DogPile',
                                                                                     'Yahoo', 'DuckDuckGo'],
                        help="Which search engine should be used? (DogPile/Bing/Google/DuckDuckGo/Yahoo)")
    parser.add_argument("-l", "--limit", help="Number of images to download.", type=int, default=100, required=False)
    parser.add_argument("--prefix", help="Filename prefix", default='', required=False)
    parser.add_argument("--postfix", help="Filename postfix", default='', required=False)
    parser.add_argument("-d", "--directory", help="Directory where to download the files", default=None, required=True)
    parser.add_argument("-c", "--chrome_driver", help="Path to Chrome driver executable. The driver can be Downloaded ",
                        default=None, required=True)
    parser.add_argument("-mw", "--min_width", help="Minimum acceptable image width", type=int, default=None,
                        required=False)
    parser.add_argument("-mh", "--min_height", help="Minimum acceptable image height", type=int, default=None,
                        required=False)
    args = parser.parse_args()
    engine = getattr(engines, args.engine)(args.chrome_driver)
    if not os.path.exists(args.directory):
        raise Exception(f'The directory does not exist: {args.directory}')
    scraper = Scraper(engine)
    scraper.download(args.search, args.directory, limit=args.limit, min_width=args.min_width,
                     min_height=args.min_height,  prefix=args.prefix, postfix=args.postfix)


if __name__ == "__main__":
    main()
