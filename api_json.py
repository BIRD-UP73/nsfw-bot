import dateutil.parser
import requests
from discord import Embed

danbooru_url = 'https://danbooru.donmai.us/posts.json'


def get_posts(tags: str, score: int):
    if 'score:>' not in tags and len(tags.split(' ')) < 2:
        tags += f' score:>={score}'

    resp_json = send_request(danbooru_url, tags)

    if len(resp_json) == 0:
        return None

    return to_embed(resp_json[0], tags)


def to_embed(post: dict, tags: str):
    embed = Embed()

    embed.set_image(url=post.get('file_url'))

    if score := post.get('score'):
        embed.add_field(name='Score', value=score)
    if artist := post.get('tag_string_artist'):
        embed.add_field(name='Artist', value=artist)
    if characters := post.get('tag_string_character'):
        embed.add_field(name='Characters', value=characters)

    embed.set_footer(text=tags)

    created_at = post.get('created_at')
    embed.timestamp = dateutil.parser.parse(created_at)

    return embed


def send_request(url, tags, random=True):
    params = {
        'limit': '1',
        'random': random,
        'tags': tags
    }

    resp = requests.get(url, params)
    resp.raise_for_status()

    return resp.json()
