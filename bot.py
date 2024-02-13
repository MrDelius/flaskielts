from telegram.ext import CommandHandler, MessageHandler, filters


# Command handler for the /start command
def start(update, bot):
    user_id = update.message.from_user.id
    bot.send_message(chat_id=user_id, text="Hello! Welcome to your bot.")


# Message handler for echoing text messages
def echo(update, bot):
    user_id = update.message.from_user.id
    text = update.message.text
    bot.send_message(chat_id=user_id, text=f"You said: {text}")


# Add the command and message handlers to the dispatcher
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(filters.TEXT, echo)
