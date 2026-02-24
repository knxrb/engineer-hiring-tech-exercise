import asyncio

import httpx
import pytest
from pytest_httpx import HTTPXMock

from src.crawler import Crawler


def test_create_async_client__returns__httpx_async_client(self):
    crawler = Crawler()

    client = crawler._create_async_client()

    assert isinstance(client, httpx.AsyncClient)


@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_check_content_type__html_is_valid_for_crawling(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=200, headers={"Content-Type": "text/html; charset=utf-8"})

    crawler = Crawler()
    crawler._limiter = asyncio.Semaphore(1)
    client = crawler._create_async_client()

    result = await crawler._check_content_type(client, 'https://www.domain.com/html')

    assert result[0] is 'https://www.domain.com/html'
    assert result[1] is True

@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_check_content_type__svg_is_not_valid_for_crawling(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=200, headers={"Content-Type": "image/svg+xml; charset=utf-8"})

    crawler = Crawler()
    crawler._limiter = asyncio.Semaphore(1)
    client = crawler._create_async_client()

    result = await crawler._check_content_type(client, 'https://www.domain.com/svg')

    assert result[0] is 'https://www.domain.com/svg'
    assert result[1] is False

@pytest.mark.asyncio
@pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
async def test_check_content_type__failure_defaults_to_valid_for_crawling(httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=500, headers={"Content-Type": "image/svg+xml; charset=utf-8"})

    crawler = Crawler()
    crawler._limiter = asyncio.Semaphore(1)
    client = crawler._create_async_client()

    result = await crawler._check_content_type(client, 'https://www.domain.com/failed')

    assert result[0] is 'https://www.domain.com/failed'
    assert result[1] is True
