from telegram import Update, Bot, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ChatAction, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence, CallbackContext
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown
import os 


TOKEN = os.environ.get('TOKEN', os.environ.get('TELEGRAM_TOKEN'))
CHAT_ID = os.environ.get('CHAT_ID', os.environ.get('TELEGRAM_CHAT_ID'))

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"Hello {user.first_name}! I'm Cyptonewscast Bot. I can send you the latest news, market and price action updates.\nTo get started, type /help")
                          

def help(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"{user.first_name}! Here are the commands I can perform:\n/start - Start the bot\n/help - Show this message\n/gainers - Show the latest gainers for the last hour")

def gainers(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"{user.first_name}! Here are the latest gainers for the last hour.") 
    update.bot.send_photo(chat_id=TOKEN, photo="https://cryptapi-news-images.ams3.digitaloceanspaces.com/gainers_1h_100.png")

def losers(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(f"{user.first_name}! Here are the latest losers for the last hour.") 
    update.message.reply_photo(photo="https://cryptapi-news-images.ams3.digitaloceanspaces.com/losers_1h_100.png")
    context.bot.send_photo(chat_id=CHAT_ID, photo="https://cryptapi-news-images.ams3.digitaloceanspaces.com/losers_1h_100.png")


def news(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    context
    

def main() -> None:
    updater = Updater(token=TOKEN, use_context=True, persistence=PicklePersistence(filename='telegram_bot_data'))
    dispatcher = updater.dispatcher

    bot = Bot(token=TOKEN)


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("gainers", gainers))
    dispatcher.add_handler(CommandHandler("losers", losers))
    dispatcher.add_handler(CommandHandler("news", news))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

