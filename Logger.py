import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

logging.getLogger('httpx').setLevel(logging.WARNING)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message_content = update.message.text
    logger.info(f'user: {user.first_name} {user.last_name} [ID: {user.id}] - msg: {message_content}')





def logrun() -> None:
    application = Application.builder().token("7059905901:AAGvPcM4lrGJjsuLiSyb_lmFjcw4mKWcsNo").build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
if __name__ == "__main__":
    logrun()