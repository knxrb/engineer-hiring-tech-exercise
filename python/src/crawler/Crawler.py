import asyncio
import warnings
from http import HTTPStatus
import httpx
from bs4 import BeautifulSoup, ResultSet, Tag, XMLParsedAsHTMLWarning
from httpx import Timeout, AsyncClient, Response

from src.crawler.URLHelper import get_clean_url, get_domain, is_scrapeable_url, from_relative_url


class Crawler:
    _concurrency_limit: int
    _base_domain: str

    _client_headers:dict = {
        'User-Agent': 'Crawler 0.1.0'
    }
    _client_timeout:Timeout = Timeout(10)

    _limiter: asyncio.Semaphore
    _current_url: str = None
    _seen: set[str] = set()
    _queue: set[str] = set()

    _output: list[str] = []

    def __init__(self, initial_url: str, concurrency_limit: int = 50) -> None:
        self._initial_url = initial_url
        self._base_domain = get_domain(initial_url)
        self._concurrency_limit = concurrency_limit
        self._limiter = asyncio.Semaphore(self._concurrency_limit)

    def create_async_client(self) -> AsyncClient:
        return httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=self._concurrency_limit,
            ),
        )

    async def run(self) -> None:
        await self.add_to_queue(self._initial_url)

        async with self.create_async_client() as client:
            while True:
                if not self._queue:
                    break

                checked_urls = await asyncio.gather(*[
                    self.check_content_type(client, url) for url in self._queue
                ])

                requests = []
                for url, is_valid_content in checked_urls:
                    if is_valid_content:
                        requests.append(self.make_request(client, url))
                    else:
                        self._seen.add(url)
                        self._queue.discard(url)

                responses = await asyncio.gather(*requests)

                for page_url, response in responses:
                    if response is not None:
                        await self.find_tags_in_response(page_url, response)


    async def check_content_type(self, client: AsyncClient, url: str) -> tuple[str, bool]:
        async with self._limiter:
            # noinspection PyBroadException
            try:
                response = await client.head(
                    url,
                    headers=self._client_headers,
                    timeout=self._client_timeout,
                )
                if response.status_code == HTTPStatus.OK:
                    content_type = response.headers.get("Content-Type", "")
                    if ';' in content_type:
                        content_type = content_type.split(';')[0]
                    return url, content_type.lower() == "text/html"

            except httpx.HTTPStatusError:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: Log the exception and continue crawling with standard max attempts retry for this URL.
                pass

            except httpx.TimeoutException:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: Log the timeout and continue crawling with exponential backoff retry for this URL.
                pass

            except:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: More specific Exception capture and log the exception for investigation.
                pass

            return url, True

    async def make_request(self, client: AsyncClient, url: str) -> tuple[str, Response | None]:
        async with self._limiter:

            self._queue.discard(url)

            # noinspection PyBroadException
            try:
                response = await client.get(
                    url,
                    headers=self._client_headers,
                    timeout=self._client_timeout,
                )
                if response.status_code == HTTPStatus.OK:
                    return url, response


            except httpx.HTTPStatusError:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: Log the exception and continue crawling with standard max attempts retry for this URL.
                pass

            except httpx.TimeoutException:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: Log the timeout and continue crawling with exponential backoff retry for this URL.
                pass

            except:
                # This coding task: We'll silently fail this URL and continue crawling.
                # Normal circumstances: More specific Exception capture and log the exception for investigation.
                pass

            return url, None

    async def find_tags_in_response(self, page_url: str, response: httpx.Response) -> None:
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(response.text, "lxml")
        found_tags = soup.find_all(href=True)
        if found_tags:
            await self.get_urls_for_found_tags(page_url, found_tags)

    async def get_urls_for_found_tags(self, page_url: str, found_tags: ResultSet[Tag]) -> None:
        print(page_url)
        for tag in found_tags:
            found_url = tag.get("href", None)
            if not await self.add_to_queue(found_url):
                await self.check_for_relative_url(page_url, found_url)

    async def check_for_relative_url(self, page_url: str, found_url: str) -> None:
        if found_url and found_url[0] == '/' or (len(found_url) > 1 and found_url[0:2] == './'):
            full_url = from_relative_url(page_url, found_url)
            await self.add_to_queue(full_url)

    async def add_to_queue(self, url: str) -> bool:
        clean_url = get_clean_url(url)
        if not is_scrapeable_url(clean_url, self._base_domain):
            return False

        if clean_url not in self._seen:
            print("-->", clean_url)
            self._seen.add(clean_url)
            self._queue.add(clean_url)
            return True

        return False
