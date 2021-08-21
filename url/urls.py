from enum import Enum


class UrlInfo:
    def __init__(self, short_url: str, long_url: str = None, cheatsheet_url: str = None):
        self.short_url = short_url
        self.long_url = long_url or f'https://{short_url}/index.php'
        self.cheatsheet_url = cheatsheet_url or f'https://{short_url}/index.php?page=help&topic=cheatsheet'

    def __hash__(self):
        return hash((self.short_url, self.long_url, self.cheatsheet_url))

    def __eq__(self, other):
        return isinstance(other, UrlInfo) \
               and self.short_url == other.short_url \
               and self.long_url == other.long_url \
               and self.cheatsheet_url == other.cheatsheet_url

    def __str__(self):
        return self.short_url


class UrlEnum(Enum):
    RULE34 = UrlInfo('rule34.xxx')
    GELBOORU = UrlInfo('gelbooru.com')
    XBOORU = UrlInfo('xbooru.com')
    TBIB = UrlInfo('tbib.org')
    DANBOORU = UrlInfo('danbooru.donmai.us', 'https://danbooru.donmai.us',
                       'https://danbooru.donmai.us/wiki_pages/help:cheatsheet')
    RULE34_PAHEAL = UrlInfo('rule34.paheal.net', long_url='https://rule34.paheal.net/api/danbooru/find_posts',
                            cheatsheet_url='https://rule34.paheal.net/help/search')
    HYPNOHUB = UrlInfo('hypnohub.net', 'https://hypnohub.net/post/index.xml?limit=1',
                       'https://hypnohub.net/help/cheatsheet')
    KONACHAN_COM = UrlInfo('konachan.com', 'https://konachan.com/post.xml', 'https://konachan.com/help/cheatsheet')
