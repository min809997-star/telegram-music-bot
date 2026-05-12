import logging
import os
import asyncio
import json
import urllib.request
import urllib.parse
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, InlineQueryHandler
from youtubesearchpython import VideosSearch
import yt_dlp

# Bot Token
TOKEN = os.environ.get('BOT_TOKEN', '8357603022:AAFLUr36aVLKZ1zIZE8LzXDdoAXmUsrDkuQ')

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
        f"🎵 Hello {user.mention_html()}! I am a Music Bot.\n\n"
        "Send me a song name and I'll find and send you the audio!\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - How to use\n"
        "/trending - Trending songs\n\n"
        "Just type any song name to get started! 🎶"
    )

# /help command handler
async def help_command(update: Update, context) -> None:
    await update.message.reply_text(
        "🎵 How to use this bot:\n\n"
        "1. Send me a song name (e.g., 'Shape of You')\n"
        "2. I'll search and send you the MP3\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/trending - Show trending songs\n\n"
        "Inline Search:\n"
        "Type @your_bot_username <song name> in any chat to search inline."
    )

# Download audio using yt-dlp with multiple fallback methods
def download_audio(video_url, video_id):
    audio_file = os.path.join('/tmp', f'{video_id}.mp3')
    
    # Method 1: Try with yt-dlp using various options
    ydl_opts_list = [
        # Method 1a: Standard download
        {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join('/tmp', f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        },
        # Method 1b: With different extractor args
        {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': os.path.join('/tmp', f'{video_id}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {'player_client': ['web', 'android']}},
        },
    ]
    
    for opts in ydl_opts_list:
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.extract_info(video_url, download=True)
            if os.path.exists(audio_file):
                return audio_file
        except Exception as e:
            logger.warning(f"Download method failed: {e}")
            continue
    
    return None

# Search and download song handler
async def search_and_send_song(update: Update, context) -> None:
    query = update.message.text
    await update.message.reply_text(f"🔍 Searching for '{query}'...")

    try:
        videosSearch = VideosSearch(query, limit=5)
        results = videosSearch.result()['result']

        if not results:
            await update.message.reply_text("❌ Sorry, I couldn't find any songs matching your query.")
            return

        video = results[0]
        video_url = video['link']
        title = video['title']
        duration = video.get('duration', 'Unknown')
        artist = video['channel']['name']
        video_id = video['id']

        await update.message.reply_text(f"🎵 Found: {title}\n🎤 {artist} ({duration})\n\n⬇️ Downloading...")

        # Try to download
        audio_file = download_audio(video_url, video_id)

        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            if file_size > 50 * 1024 * 1024:  # Telegram limit is 50MB
                await update.message.reply_text("❌ File too large for Telegram. Try a shorter song.")
                os.remove(audio_file)
                return
            
            await update.message.reply_audio(
                audio=open(audio_file, 'rb'),
                title=title,
                performer=artist,
                duration=parse_duration(duration)
            )
            os.remove(audio_file)
        else:
            # If download fails, send the YouTube link instead
            await update.message.reply_text(
                f"⚠️ Download not available right now.\n\n"
                f"🎵 {title}\n"
                f"🎤 {artist}\n"
                f"⏱ {duration}\n"
                f"🔗 {video_url}\n\n"
                f"You can listen/download from the link above."
            )

    except Exception as e:
        logger.error(f"Error searching or downloading song: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again later.")

# Helper function to parse duration string to seconds
def parse_duration(duration_str):
    if not duration_str or duration_str == 'Unknown':
        return 0
    try:
        parts = duration_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    except:
        pass
    return 0

# /trending command handler
async def trending(update: Update, context) -> None:
    await update.message.reply_text("🔥 Fetching trending songs...")
    try:
        videosSearch = VideosSearch("top music hits 2026", limit=10)
        results = videosSearch.result()['result']

        if not results:
            await update.message.reply_text("Could not fetch trending songs at the moment.")
            return

        message_text = "🔥 Trending Songs:\n\n"
        for i, video in enumerate(results):
            message_text += f"{i+1}. 🎵 {video['title']}\n"
            message_text += f"   🎤 {video['channel']['name']} ({video.get('duration', '')})\n\n"
        await update.message.reply_text(message_text)

    except Exception as e:
        logger.error(f"Error fetching trending songs: {e}")
        await update.message.reply_text("❌ An error occurred while fetching trending songs.")

# Inline query handler
async def inline_query(update: Update, context) -> None:
    query = update.inline_query.query
    if not query:
        return

    results = []
    try:
        videosSearch = VideosSearch(query, limit=5)
        yt_results = videosSearch.result()['result']
        for i, video in enumerate(yt_results):
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=video['title'],
                    input_message_content=InputTextMessageContent(
                        f"🎵 {video['title']}\n🎤 {video['channel']['name']}\n🔗 {video['link']}"
                    ),
                    description=f"{video['channel']['name']} - {video.get('duration', '')}"
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

    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
