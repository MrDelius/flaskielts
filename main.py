# import asyncio
# from asyncio import queues
# import logging

from flask import Flask, request, Response, jsonify
from flask_restful import Api
from models import db
from speaking import SpeakingQueries
from user import UserQueries
from speaking_token import TokenQueries
# from telegram import Bot, Update, Message
# from telegram.ext import Application, Updater, CallbackContext, CommandHandler, MessageHandler, filters

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

api.add_resource(SpeakingQueries, '/speaking/<int:task_id>', endpoint='speaking_queries_put')
api.add_resource(SpeakingQueries, '/speaking/', endpoint='speaking_queries')

api.add_resource(UserQueries, '/user/<int:user_id>', endpoint='user_queries')
api.add_resource(UserQueries, '/user/<int:chat_id>', endpoint='user_queries_get')

api.add_resource(TokenQueries, '/token/', endpoint='token_queries_post')
api.add_resource(TokenQueries, '/token/<string:token>', endpoint='token_queries')

# Enable logging
"""logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '5581794924:AAE-9g3zDg546E43itu-gONgOoChbEltGN8'
bot = Bot(token=TOKEN)
updater = Updater(bot=TOKEN, update_queue=queues.Queue())
application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: CallbackContext) -> Message:
    await update.message.reply_text('Hello! I am your bot.')


async def echo(update: Update, context: CallbackContext) -> Message:
    await update.message.reply_text(update.message.text)


# Error handler to handle the AttributeError
def error_handler(update: Update, context: CallbackContext) -> None:
    logging.error(f'Error: {context.error}')


@app.route('/', methods=['GET'])
def default():
    return Response('Get ok', status=200)


@app.route('/webhook', methods=["POST", "GET"])
async def telegram_webhook():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        update = Update.de_json(data, bot)
        print(update)
        await bot.initialize()
        await application.initialize()

        # Add command handlers
        start_handler = CommandHandler('start', start)
        echo_handler = MessageHandler(filters.TEXT, echo)

        application.add_handler(start_handler)
        application.add_handler(echo_handler)

        await application.process_update(update)
        return 'OK', 200

    return Response('OK', status=200)
"""

@app.route('/', methods=['GET'])
def default():
    return Response('Get ok', status=200)


if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(bot.setWebhook('https://3a3f-84-54-122-153.ngrok-free.app/webhook'))
    app.run(debug=False)
