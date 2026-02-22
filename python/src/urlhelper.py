from urllib.parse import urlparse, urlunparse, urljoin


def is_valid_url(url: str) -> bool:
    """
    Determine if the provided URL is valid by checking
    the presence of both a scheme and hostname.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL has a scheme and hostname; otherwise, False.
    """
    parsed_url = urlparse(url)
    return True if parsed_url.scheme and parsed_url.hostname else False


def is_same_domain(url: str, domain: str) -> bool:
    """
    Check if a given URL belongs to the specified domain.

    This function compares the domain extracted from the provided URL
    with the given domain and determines if they match.

    Args:
        url: The URL to check.
        domain: The domain to compare against.

    Returns:
        True if the URL domain matches the given domain; otherwise, False.
    """
    return domain == get_domain(url)


def get_domain(url: str) -> str:
    """
    Extract the domain from a given URL.

    This function uses the urlparse method to parse the URL and
    returns the hostname component, which represents the domain.

    Args:
        url: A string representing the URL to extract the domain from.

    Returns:
        The hostname extracted from the URL.
    """
    # I'd use .netloc if scope limitation needs to consider the port number.
    # For example, when crawling a site that uses an IP address, such as https://192.168.1.10:8024
    return urlparse(url).hostname


def get_clean_url(url: str) -> str:
    """
    Clean a URL by removing any trailing slashes and removing any
    querystring parameters or other unneeded parts.

    Args:
        url: The URL to clean.

    Returns:
        The cleaned URL.
    """
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


def is_crawlable_url(url: str | None, domain: str) -> bool:
    """
    Determine if a URL is a valid URL for crawling based on the presence of a
    scheme, hostname, and it being in the same domain as the specified domain.

    Args:
        url: The URL to check.
        domain: The domain to compare against.

    Returns:
        True if the URL is valid and matches the specified domain; otherwise, False.
    """
    return url is not None and is_valid_url(url) and is_same_domain(url, domain)


def from_relative_url(origin_url: str, relative_url: str | None) -> str:
    """
    Constructs a full URL from an origin URL and a relative URL; replacing parts
    of the origin URL with matching parts from the relative URL, where necessary.

    Args:
        origin_url: The initial URL for the crawling session.
        relative_url: The relative URL to combine with the origin URL.

    Returns:
        The combined URL.
    """
    full_url = urljoin(origin_url, relative_url)
    clean_url = get_clean_url(full_url)
    return clean_url
