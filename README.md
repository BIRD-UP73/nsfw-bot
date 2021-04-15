# nsfw-bot
A Discord bot that posts NSFW images.

## How to run
- In the main directory add a file named `config.properties` and fill it with a bot token and a default prefix
```proprties
[DEFAULT]
token=birdup
prefix=!
```
- Run `launcher.py`

**Note:** enable the **Members** intent for the bot to work in DMs

## Supported sites
Warning! These sites contain NSFW content.

- rule34.xxx
- gelbooru.com
- xbooru.com
- tbib.org
- danbooru.donmai.us

## Emojis used
- ⬅ and ➡ to cycle through pages
- 🗑️ to delete post messages or favorites
- ⭐ to store a post as favorite
- 🔁 to refresh posts
- ⛔ to remove a favorite

## A note on reactions
Removing reactions of other others in DMs is not allowed for bots.
Therefore the bot will not automatically remove reactions in DMs.
