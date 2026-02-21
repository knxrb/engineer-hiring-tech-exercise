import asyncio
import sys

from src.crawler.Crawler import Crawler


async def main(url: str):
	crawler = Crawler(url)
	await crawler.run()


if __name__ == '__main__':
	args = sys.argv[1:]
	asyncio.run(main(args[0]))
