from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import subprocess
import os
import logging

application = Application.builder().token("7059905901:AAGvPcM4lrGJjsuLiSyb_lmFjcw4mKWcsNo").build()


async def spotDL(update: Update, context: ContextTypes):
    if context.args:
        link = context.args[0]
        try:
            subprocess.run(f'spotdl --output "C:/Users/jezip/Telegram-bot/songdebug" --bitrate 320K {link}', shell=True)
        except Exception as e:
            if update.message:
                await update.message.reply_text(f"Error downloading track: {str(e)}")
            return
        track_name = link.split('/')[-1]
        if os.path.exists(track_name):
            with open(track_name, "rb") as audio:
                await update.message.reply_audio(audio)
            os.remove(track_name)
            if update.message:
                await update.message.reply_text("Your MP3 file has been uploaded!")
        else:
            if update.message:
                await update.message.reply_text("Failed to download the track. Please try again later.")
    else:
        if update.message:
            await update.message.reply_text("Please provide a link to download a track.")


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


application.add_handler(MessageHandler(filters.TEXT, log))
spotify_dl_handler = CommandHandler("spotDL", spotDL)
application.add_handler(spotify_dl_handler)
if __name__ == "__main__":
    application.run_polling(allowed_updates=Update.ALL_TYPES)