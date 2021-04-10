from urllib.parse import urlparse

from urls import danbooru, gelbooru, rule34, tbib, xbooru, danbooru_full_url

short_urls = {
    'danbooru': danbooru,
    'gelbooru': gelbooru,
    'rule34': rule34,
    'tbib': tbib,
    'xbooru': xbooru
}


def parse_url(url: str) -> str:
    parsed_url = urlparse(url).hostname or url

    if 'donmai.us' in parsed_url:
        return danbooru

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
        return 'https://danbooru.donmai.us/wiki_pages/help:cheatsheet'

    short_url = short_urls.get(command_name)
    return f'https://{short_url}/index.php?page=help&topic=cheatsheet'
