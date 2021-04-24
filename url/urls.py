class URL:
    short_url: str = ''
    long_url: str = ''
    cheatsheet_url: str = ''

    @staticmethod
    def find(url: str):
        if url == Rule34.short_url:
            return Rule34
        if url == Gelbooru.short_url:
            return Gelbooru
        if url == Xbooru.short_url:
            return Xbooru
        if url == Tbib.short_url:
            return Tbib
        if url == Danbooru.short_url:
            return Danbooru
        if url == Rule34Paheal.short_url:
            return Rule34Paheal
        if url == Hypnohub.short_url:
            return Hypnohub

    @staticmethod
    def create_api_params(**kwargs):
        return kwargs


class DefaultURL(URL):
    def __init__(self, short_url: str):
        self.short_url = short_url
        self.long_url = f'https://{short_url}/index.php'
        self.cheatsheet_url = f'https://{short_url}/index.php?page=help&topic=cheatsheet'

    @staticmethod
    def create_api_params(**kwargs):
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'limit': kwargs.get('limit')
        }
        if post_id := kwargs.get('id'):
            params['id'] = post_id
        if tags := kwargs.get('tags'):
            params['tags'] = tags
        if page := kwargs.get('page'):
            params['pid'] = page

        return params


class Rule34Paheal(URL):
    short_url = 'rule34.paheal.net'
    long_url = 'https://rule34.paheal.net/api/danbooru/find_posts'
    cheatsheet_url = 'https://rule34.paheal.net/help/search'


class Danbooru(URL):
    short_url = 'danbooru.donmai.us'
    long_url = 'https://danbooru.donmai.us'
    cheatsheet_url = 'https://danbooru.donmai.us/wiki_pages/help:cheatsheet'


class Hypnohub(URL):
    short_url = 'hypnohub.net'
    long_url = 'https://hypnohub.net/post/index.xml?limit=1'
    cheatsheet_url = 'https://hypnohub.net/help/cheatsheet'


Rule34 = DefaultURL('rule34.xxx')
Gelbooru = DefaultURL('gelbooru.com')
Xbooru = DefaultURL('xbooru.com')
Tbib = DefaultURL('tbib.org')
