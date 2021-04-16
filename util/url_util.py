from urllib.parse import urlparse

from url.urls import URL


def parse_url(url: str) -> str:
    parsed_url = urlparse(url).hostname or url

    if 'donmai.us' in parsed_url:
        return URL.DANBOORU.short_url

    split_hostname = parsed_url.split('.')

    if len(split_hostname) > 2:
        return '.'.join(split_hostname[-2:])

    return parsed_url


def short_to_long(short_url: str) -> str:
    if short_url in URL.DANBOORU.long_url:
        return URL.DANBOORU.long_url

    return f'https://{short_url}/index.php'
