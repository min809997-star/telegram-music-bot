
import logging
import os
import asyncio
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, InlineQueryHandler
from youtube_search import YoutubeSearch
import yt_dlp

# Bot Token (replace with your actual token)
TOKEN = '8357603022:AAFLUr36aVLKZ1zIZE8LzXDdoAXmUsrDkuQ'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"Hello {user.mention_html()}! I am a music bot. Send me a song name to get its audio."
        "\n\nHere are the commands you can use:\n"
        "/start - Get a welcome message\n"
        "/help - Get instructions on how to use the bot\n"
        "/trending - Get a list of trending songs\n"
        "You can also use inline search by typing `@your_bot_username song name` in any chat."
    )

# /help command handler
async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "To use this bot, simply send me the name of a song you want to download. "
        "I will search YouTube, download the audio, and send it to you as an MP3 file.\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help message\n"
        "/trending - Show a list of trending songs\n\n"
        "Inline Search:\n"
        "In any chat, type `@your_bot_username <song name>` to search for songs inline and share them."
    )

# Search and download song handler
async def search_and_send_song(update: Update, context) -> None:
    query = update.message.text
    await update.message.reply_text(f"Searching for '{query}'...")

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await update.message.reply_text("Sorry, I couldn't find any songs matching your query.")
            return

        video = results[0]
        video_url = f"https://www.youtube.com{video['url_suffix']}"
        title = video['title']
        duration = video['duration']
        artist = video['channel']

        await update.message.reply_text(f"Found: {title} by {artist} ({duration}). Downloading...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join('/tmp', f'{video["id"]}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        if os.path.exists(audio_file):
            await update.message.reply_audio(
                audio=open(audio_file, 'rb'),
                title=title,
                performer=artist,
                duration=parse_duration(duration)
            )
            os.remove(audio_file)
        else:
            await update.message.reply_text("Failed to download the audio file.")

    except Exception as e:
        logger.error(f"Error searching or downloading song: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

# Helper function to parse duration string to seconds
def parse_duration(duration_str):
    parts = duration_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

# /trending command handler (placeholder)
async def trending(update: Update, context) -> None:
    await update.message.reply_text("Fetching trending songs...")
    try:
        # This is a simplified approach. YouTube's official API would be better for true trending.
        # For now, we'll search for popular music videos.
        results = YoutubeSearch("trending music videos", max_results=10).to_dict()
        if not results:
            await update.message.reply_text("Could not fetch trending songs at the moment.")
            return

        message_text = "Here are some trending songs:\n\n"
        for i, video in enumerate(results):
            message_text += f"{i+1}. {video['title']} by {video['channel']} ({video['duration']})\n"
            message_text += f"https://www.youtube.com{video['url_suffix']}\n\n"
        await update.message.reply_text(message_text)

    except Exception as e:
        logger.error(f"Error fetching trending songs: {e}")
        await update.message.reply_text("An error occurred while fetching trending songs. Please try again later.")

# Inline query handler (placeholder)
async def inline_query(update: Update, context) -> None:
    query = update.inline_query.query
    if not query:
        return

    results = []
    try:
        yt_results = YoutubeSearch(query, max_results=5).to_dict()
        for i, video in enumerate(yt_results):
            video_url = f"https://www.youtube.com{video['url_suffix']}"
            results.append(
                InlineQueryResultArticle(
                    id=video['id'],
                    title=video['title'],
                    input_message_content=InputTextMessageContent(video['title']),
                    description=f"{video['channel']} - {video['duration']}"
                )
            )
    except Exception as e:
        logger.error(f"Error in inline query: {e}")

    await update.inline_query.answer(results)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("trending", trending))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_and_send_song))
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
