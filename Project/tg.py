from pyrogram import Client, filters
from pyrogram.enums import ChatType
from main_bridge import message_queue, Message, MediaFile


def create_telegram_bridge(TELEGRAM_TOKEN, API_ID, API_HASH):
    app = Client(
        name='telegram_bridge',
        bot_token=TELEGRAM_TOKEN,
        api_hash=API_HASH,
        api_id=API_ID,
        ipv6=False,
    )

    @app.on_message(filters.group)
    async def on_message(client, message):
        text = message.text or message.caption or ""

        msg = Message(
            source='telegram',
            username=message.from_user.first_name if message.from_user else "Аноним",
            text=text)

        if message.media:
            media_file = None

            if message.animation:
               media_file = MediaFile(
                   file_id=message.animation.file_id,
                   type='gif',
                   duration=message.animation.duration,
               )
            elif message.photo:
               media_file = MediaFile(
                   file_id=message.photo.file_id,
                   type='photo'
               )
            elif message.video:
               media_file = MediaFile(
                   file_id=message.video.file_id,
                   type='video',
                   duration=message.video.duration,
               )
            elif message.sticker:
                media_file = MediaFile(
                    file_id=message.sticker.file_id,
                    type='photo',
                )
            elif message.video_note:
                media_file = MediaFile(
                    file_id=message.video_note.file_id,
                    type='video',
                    duration=message.video_note.duration
                )

            if media_file:
                msg.media.append(media_file)

        await message_queue.put(msg)

    return app


