import asyncio
import io
import os
import tempfile

import aiohttp
import discord as ds
from main_bridge import MediaFile, Message, message_queue
from pyrogram.enums import ChatType


class MessageProcessor:
    def __init__(self, telegram_bot, discord_bot, DISCORD_GUILD, DISCORD_CHANNEL, TELEGRAM_CHAT):
        self.telegram_bot = telegram_bot
        self.discord_bot = discord_bot
        self.DISCORD_GUILD = int(DISCORD_GUILD)
        self.DISCORD_CHANNEL = int(DISCORD_CHANNEL)
        self.TELEGRAM_CHAT = int(TELEGRAM_CHAT)

    async def process(self):
        print("[QP] process() ЗАПУЩЕН! Жду сообщения...")
        while True:
            try:
                msg = await message_queue.get()
                print(f"[QP] ПОЛУЧЕНО: source={msg.source}, текст={msg.text[:30] if msg.text else 'пусто'}, медиа={len(msg.media)}")

                if msg.source == 'telegram':
                    await self.send_to_discord(msg)
                elif msg.source == 'discord':
                    await self.send_to_telegram(msg)

                message_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                message_queue.task_done()

    async def send_to_discord(self, msg: Message):
        channel = None
        for guild in self.discord_bot.guilds:
            if str(guild.id) == str(self.DISCORD_GUILD):
                for ch in guild.text_channels:
                    if str(ch.id) == str(self.DISCORD_CHANNEL):
                        channel = ch
                        break
                if channel:
                    break

        if not channel:
            return

        files_to_send = []
        for media in msg.media:
            if media.file_id:
                try:
                    print(f"[QP] Скачивание медиа: {media.type} (file_id: {media.file_id[:8]}...)")
                    file_path = await self.download_telegram_media(media)
                    if file_path:
                        files_to_send.append((file_path, media.type))
                        print(f"[QP] Скачано: {file_path}")
                except Exception as e:
                    print(f'Ошибка скачивания! {e}')

        if msg.text and not files_to_send:
            print(f"[QP] Отправка текста в Discord: {msg.text[:50]}...")
            await channel.send(f'{msg.username}: {msg.text}')
        elif msg.text and files_to_send:
            await channel.send(f'{msg.username}: {msg.text}')
            for file_path, media_type in files_to_send:
                await self.send_file_to_discord(channel, file_path, media_type)
        elif files_to_send:
            await channel.send(f'{msg.username}')
            for file_path, media_type in files_to_send:
                await self.send_file_to_discord(channel, file_path, media_type)
        else:
            print("⚠️ [QP] Пустое сообщение (нет текста и нет медиа)")

    async def send_file_to_discord(self, channel, file_path, media_type):
        print(f"[QP] send_file_to_discord: {file_path} (тип: {media_type})")
        try:
            discord_file = ds.File(file_path)
            if media_type == "gif" or media_type == "video" or media_type == "photo":
                await channel.send(file=discord_file)
            else:
                await channel.send(file=discord_file)
        except Exception as e:
            print(f'Ошибка отправки файла: {e}')
        finally:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                os.rmdir(os.path.dirname(file_path))
            except Exception:
                pass

    async def download_telegram_media(self, media: MediaFile):
        print(f"[QP] download_telegram_media: {media.type}")
        temp_dir = tempfile.mkdtemp()
        file_name = f"file"
        if media.type == 'gif':
            file_name = f'{file_name}.mp4'
        elif media.type == 'photo':
            file_name = f'{file_name}.jpg'
        elif media.type == 'video':
            file_name = f'{file_name}.mp4'
        else:
            file_name = f'{file_name}.file'

        file_path = os.path.join(temp_dir, file_name)

        try:
            await self.telegram_bot.download_media(
                message=media.file_id,
                file_name=file_path
            )
            return file_path
        except Exception as e:
            print(f'[QP] Ошибка скачивания из Telegram: {e}')
            return None

    async def send_to_telegram(self, msg: Message):
        print(f"[QP] send_to_telegram: текст={msg.text[:30] if msg.text else 'пусто'}, медиа={len(msg.media)}")

        if msg.text:
            try:
                await self.telegram_bot.send_message(
                    chat_id=self.TELEGRAM_CHAT,
                    text=f'{msg.username}: {msg.text}'
                )
            except Exception as e:
                print(f"[QP] Ошибка отправки текста: {e}")

        for media in msg.media:
            if media.url:
                try:
                    await self.send_media_to_telegram(media, msg.username)
                except Exception as e:
                    print(f'[QP] Ошибка отправки медиа: {e}!')

    async def send_media_to_telegram(self, media: MediaFile, username):

        try:
            file_data, media_type = await self.download_discord_media(media.url)

            if not file_data or not media_type:
                return

            file_obj = io.BytesIO(file_data)
            file_obj.name = "file." + media_type[6:] if media_type and len(media_type) > 6 else "file.jpg"

            if media_type == "gif" or (media_type and media_type.endswith("gif")):
                await self.telegram_bot.send_animation(
                    chat_id=self.TELEGRAM_CHAT,
                    animation=file_obj,
                    caption=f'{username}'
                )

            elif media_type == "video" or (media_type and media_type.startswith("video/")):
                await self.telegram_bot.send_video(
                    chat_id=self.TELEGRAM_CHAT,
                    video=file_obj,
                    caption=f'{username}'
                )

            elif media_type == "webp" or (media_type and media_type.endswith("webp")):
                await self.telegram_bot.send_photo(
                    chat_id=self.TELEGRAM_CHAT,
                    photo=file_obj,
                    caption=f'{username}'
                )

            elif media_type == "photo" or (media_type and media_type.startswith("image/")):
                await self.telegram_bot.send_photo(
                    chat_id=self.TELEGRAM_CHAT,
                    photo=file_obj,
                    caption=f'{username}'
                )
            else:
                await self.telegram_bot.send_document(
                    chat_id=self.TELEGRAM_CHAT,
                    document=file_obj,
                    caption=f'{username}'
                )

        except Exception as e:
            print(f'[QP] Ошибка в send_media_to_telegram: {e}')

    async def download_discord_media(self, url):
        print(f"[QP] download_discord_media: {url[:60]}...")
        attempts = 5
        for attempt in range(attempts):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            file_data = await response.read()
                            file_type = response.headers.get('Content-type', '')
                            print(f"[QP] Скачано: {len(file_data)} байт, тип: {file_type}")
                            return file_data, file_type
                        else:
                            print(f"[QP] Ошибка скачивания: HTTP {response.status}; Попытка: {attempt + 1}")
                            print(f"URL: {url}")
                            await asyncio.sleep(2)
                            continue
            except Exception as e:
                print(f'[QP] Ошибка скачивания из Discord: {e}; Попытка: {attempt + 1}')
                await asyncio.sleep(1)
                continue
        return None, None