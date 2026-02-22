from urllib.parse import urlparse, urlunparse, urljoin


def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return True if parsed_url.scheme and parsed_url.netloc else False


def is_same_domain(url: str, domain: str) -> bool:
    return domain == get_domain(url)


def get_domain(url: str) -> str:
    # I'd use .netloc if scope limitation needs to consider the port number.
    # For example, when crawling a site that uses an IP address, such as https://192.168.1.10:8024
    return urlparse(url).hostname


def get_clean_url(url: str) -> str:
    parsed_url = urlparse(url)
    cleaned_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            '',
            '',
            '',
        ),
    )
    if cleaned_url.endswith('/'):
        cleaned_url = cleaned_url[:-1]
    return cleaned_url


def is_scrapeable_url(url: str | None, domain: str) -> bool:
    return url is not None and is_valid_url(url) and is_same_domain(url, domain)


def from_relative_url(origin_url: str, relative_url: str | None) -> str:
    full_url = urljoin(origin_url, relative_url)
    clean_url = get_clean_url(full_url)
    return clean_url
