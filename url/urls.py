from enum import Enum


class URL(Enum):
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, short_url: str, long_url: str = None, cheatsheet_url: str = None):
        self.short_url = short_url
        self.long_url = long_url
        self.cheatsheet_url = cheatsheet_url

    RULE34 = 'rule34.xxx'
    GELBOORU = 'gelbooru.com'
    XBOORU = 'xbooru.com'
    TBIB = 'tbib.org'
    DANBOORU = 'danbooru.donmai.us', 'https://danbooru.donmai.us',\
               'https://danbooru.donmai.us/wiki_pages/help:cheatsheet'

    @property
    def long_url(self):
        if self._long_url:
            return self._long_url

        return f'https://{self.short_url}/index.php'

    @long_url.setter
    def long_url(self, value):
        self._long_url = value

    @property
    def cheatsheet_url(self):
        if self._cheatsheet_url:
            return self._cheatsheet_url

        return f'https://{self.short_url}/index.php?page=help&topic=cheatsheet'

    @cheatsheet_url.setter
    def cheatsheet_url(self, value):
        self._cheatsheet_url = value
