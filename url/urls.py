
class URL:
    short_url: str = ''
    long_url: str = ''
    cheatsheet_url: str = ''

    def __init__(self, short_url: str):
        self.short_url = short_url
        self.long_url = f'https://{short_url}/index.php'
        self.cheatsheet_url = f'https://{short_url}/index.php?page=help&topic=cheatsheet'


class Danbooru(URL):
    short_url = 'danbooru.donmai.us'
    long_url = 'https://danbooru.donmai.us'
    cheatsheet_url = 'https://danbooru.donmai.us/wiki_pages/help:cheatsheet'


class Hypnohub(URL):
    short_url = 'hypnohub.net'
    long_url = 'hypnohub.net/post/index.xml'
    cheatsheet_url = 'https://hypnohub.net/help/cheatsheet'


Rule34 = URL('rule34.xxx')
Gelbooru = URL('gelbooru.com')
Xbooru = URL('xbooru.com')
Tbib = URL('tbib.org')

print(Danbooru.long_url)
