from urllib.parse import urlparse


short_urls = {
    'rule34': 'rule34.xxx',
    'gelbooru': 'gelbooru.com',
    'xbooru': 'xbooru.com',
    'tbib': 'tbib.org',
    'danbooru': 'danbooru.donmai.us'
}


def parse_url(url: str) -> str:
    return urlparse(url).hostname or url


def short_to_long(short_url):
    if short_url == 'danbooru.donmai.us':
        return 'https://danbooru.donmai.us/posts'

    return f'https://{short_url}/index.php'


def get_long_url(command_name: str):
    return short_to_long(short_urls.get(command_name))
