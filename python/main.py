import asyncio
import sys

from src.crawler import Crawler


async def main(url: str):
    crawler = Crawler()
    await crawler.run(url)


if __name__ == '__main__':
    args = sys.argv[1:]
    asyncio.run(main(args[0]))
