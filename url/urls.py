from typing import Dict


class URL:
    short_url: str = ''
    long_url: str = ''
    cheatsheet_url: str = ''
    api_options: Dict = {}

    @staticmethod
    def find(url: str):
        if url == 'rule34.xxx':
            return Rule34
        if url == 'gelbooru.com':
            return Gelbooru
        if url == 'xbooru.com':
            return Xbooru
        if url == 'tbib.org':
            return Tbib
        if url == 'danbooru.donmai.us':
            return Danbooru


class DefaultURL(URL):
    api_options = {
        'page': 'dapi',
        's': 'post',
        'q': 'index'
    }

    def __init__(self, short_url: str):
        self.short_url = short_url
        self.long_url = f'https://{short_url}/index.php'
        self.cheatsheet_url = f'https://{short_url}/index.php?page=help&topic=cheatsheet'


class Danbooru(URL):
    short_url = 'danbooru.donmai.us'
    long_url = 'https://danbooru.donmai.us'
    cheatsheet_url = 'https://danbooru.donmai.us/wiki_pages/help:cheatsheet'


Rule34 = DefaultURL('rule34.xxx')
Gelbooru = DefaultURL('gelbooru.com')
Xbooru = DefaultURL('xbooru.com')
Tbib = DefaultURL('tbib.org')
