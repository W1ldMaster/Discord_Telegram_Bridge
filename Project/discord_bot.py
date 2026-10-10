import re

import discord as ds
from discord.ext import commands
from main_bridge import MediaFile, Message, message_queue


def create_discord_bot(DISCORD_CHANNEL):
    intents = ds.Intents.default()

    intents.message_content = True
    intents.members = True
    intents.presences = True

    bot = commands.Bot(command_prefix='p! ', intents=intents)

    @bot.event
    async def on_message(message):
        try:
            if message.content[:2] == 'p!':
                await bot.process_commands(message)
                return
            elif message.author.id == bot.user.id:
                return
            else:
                if str(message.channel.id) == str(DISCORD_CHANNEL):
                    msg = Message(
                        source='discord',
                        username=message.author.nick or message.author.name,
                        text=message.content
                    )
                    if message.embeds:
                        embed = message.embeds[0]
                        media = MediaFile(
                            url=embed.thumbnail.url or embed.image.url or embed.url,
                            type='gif'
                        )
                        msg.text = ''
                        msg.media.append(media)
                    elif 'https://' in message.content and 'gif' in message.content:
                        idmatch = ''
                        if 'tenor' in message.content:
                            idmatch = (re.search(r'view/[^/]+-(\d+)', url)).group(1)
                            msg.text = f"https://media.tenor.com/{gif_id}/tenor.gif"

                        elif 'giphy' in message.content:
                            idmatch = (re.search(r'giphy\.com/gifs/([a-zA-Z0-9_-]+)', url)).group(1)
                            msg.text = f"https://media.giphy.com/media/{gif_id}/giphy.gif"

                        media = MediaFile(
                            url=msg.text,
                            type='gif'
                        )
                        msg.text = ''
                        msg.media.append(media)
                    if message.attachments:
                        for attachment in message.attachments:
                            media_type = None
                            if attachment.content_type:
                                if attachment.content_type.startswith('image/'):
                                    media_type = 'photo'
                                elif attachment.content_type.startswith('video/'):
                                    media_type = 'video'
                            if attachment.filename and attachment.filename.lower().endswith('.gif'):
                                media_type = 'gif'

                            media = MediaFile(
                                url=attachment.url,
                                type=media_type
                            )
                            msg.media.append(media)
                    await message_queue.put(msg)
            await bot.process_commands(message)
        except Exception as e:
            print(f'Ошибка: {e}!')

    return bot
