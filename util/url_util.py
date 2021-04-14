from urllib.parse import urlparse

from url.urls import URL


def parse_url(url: str) -> str:
    parsed_url = urlparse(url).hostname or url

    if 'donmai.us' in parsed_url:
        return URL.DANBOORU

    split_hostname = parsed_url.split('.')

    if len(split_hostname) > 2:
        return '.'.join(split_hostname[-2:])

    return parsed_url


def short_to_long(short_url: str) -> str:
    if short_url in danbooru:
        return danbooru_full_url

    return f'https://{short_url}/index.php'


def get_long_url(command_name: str):
    return short_to_long(short_urls.get(command_name))


def cheat_sheet_url(command_name: str):
    if command_name == 'danbooru':
        return

    short_url = short_urls.get(command_name)
    return
