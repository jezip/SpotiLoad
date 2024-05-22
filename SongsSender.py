from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import subprocess
import os
import logging

application = Application.builder().token("").build()
directory = 'C:\\Users\\jezip\\Telegram-bot\\songdebug'


async def welcome(update: Update, context: ContextTypes):
  message = "Welcome to @SpotiLoadMusicBot\nUse /d [link] to download your desired track.\nThe bot also supports track recognition by title."
  await update.message.reply_text(message)


async def spotify_dl(update: Update, context: ContextTypes):
    if context.args:
        link = "-".join(context.args)
        try:
            subprocess.run(f'spotdl --output "C:/Users/jezip/Telegram-bot/songdebug" --bitrate 320K {link}', shell=True)
        except Exception as e:
            if update.message:
                await update.message.reply_text(f"Error downloading track: {str(e)}")
            return

#============================================================================================================

        def list_mp3_files(directory):
            mp3_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.mp3'):
                        mp3_files.append(file)

            return mp3_files

        if __name__ == "__main__":
          mp3_files = list_mp3_files(directory)
          if mp3_files:
            for track_name in mp3_files:
              if os.path.exists(os.path.join(directory, track_name)):
                with open(os.path.join(directory, track_name), "rb") as audio:
                  await update.message.reply_audio(audio)
                os.remove(os.path.join(directory, track_name))
              else:
                if update.message:
                  await update.message.reply_text(f"Failed to find the track: {track_name}. Please try again.")
          else:
            if update.message:
              await update.message.reply_text("No MP3 files found in the directory.")


#============================================================================================================
#============================================================================================================


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger('httpx').setLevel(logging.WARNING)

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message_content = update.message.text
    logger.info(f'user: {user.first_name} {user.last_name} [ID: {user.id}] - msg: {message_content}')


#============================================================================================================
#============================================================================================================


welcome_handler = CommandHandler("start", welcome)
application.add_handler(welcome_handler)
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, log))
spotify_dl_handler = CommandHandler("d", spotify_dl)
application.add_handler(spotify_dl_handler)
if __name__ == "__main__":
    application.run_polling(allowed_updates=Update.ALL_TYPES)
