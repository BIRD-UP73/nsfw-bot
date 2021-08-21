from xml.etree import ElementTree

import xmlschema
from discord.ext.commands import UserInputError

from posts.api.rule34_api import Rule34Api
from posts.config.configuration import Configuration
from url.urls import UrlEnum


class Rule34Config(Configuration):
    url_info = UrlEnum.RULE34
    api = Rule34Api()

    def fetch_count(self, query: str):
        # Fetch 0 posts to just get the post count
        api_params = self.api.create_api_params(query)
        resp = self.api.send_request(api_params)

        resp_text = resp.text

        my_schema = xmlschema.XMLSchema('./counts_response.xsd')
        my_schema.validate(resp_text)

        posts = ElementTree.fromstring(resp_text)

        text_count = posts.get('count')
        int_count = int(text_count)
        count = min(self.max_posts or int_count, int_count)

        if count == 0:
            raise UserInputError(f'Could not find posts for {query}')

        return count
