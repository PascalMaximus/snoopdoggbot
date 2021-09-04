import logging
import os
import re
import requests
from bs4 import BeautifulSoup as bs
from gtts import gTTS
from uuid import uuid4
from functools import wraps
from config import BOT_TOKEN
from telegram import *
from telegram.ext import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = BOT_TOKEN
bot = Bot(BOT_TOKEN)

#  Decorator for chat actions
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=action
            )
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


def gizoogle(input_text):
    params = {"translatetext": input_text}
    target_url = "http://www.gizoogle.net/textilizer.php"
    r = requests.post(target_url, data=params)
    soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', r.text)
    soup = bs(soup_input, "lxml")
    giz = soup.find_all(text=True)
    giz_text = giz[37].strip("\r\n")
    return giz_text


@send_action(ChatAction.TYPING)
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton(
                "Source code", url="https://github.com/pascalmaximus/snoopdoggbot"
            ),
            InlineKeyboardButton(
                "Join Mah Channel", url="https://telegram.dog/botivity"
            ),
        ],
        [InlineKeyboardButton("Use me inline 🐾 ", switch_inline_query_current_chat="")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    user_says = " ".join(context.args)
    if user_says == "sourcecode":
        update.message.reply_text(
            "[SourceCode](https://github.com/pascalmaximus/snoopdoggbot)\nBrought to you by @botivity",
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_markdown_v2(
            fr"Yo whatsup {user.mention_markdown_v2()} rap wit me or i will kick you read /pg13 before using please and join ma channel  @botivity\!",
            reply_markup=reply_markup,
        )


# In case snoopdogg uses too much explicit language (just a precaution also this is copied from gizoogle.net you can find it there minor modifications are made though)
@send_action(ChatAction.TYPING)
def pg13(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        " <u>Some Obscene Language</u>\n\nThis bot is only intended for mature audiences farmiliar with the gangsta slang used by Snoop Dogg, and anybody under the age of 13 should not even think about using this bot without adult supervision.\nApologies if you are in any way offended by the explicit wording used in the translations.\nThe slanguage used in our algorithm has been quoted from Snoop Dogg himself and is commonly used in movies, conversations and music he has written.\nThese words are based on slang and can not be interpreted in any other way other than how they are quoted. There are no racist words used in the algorithm.\nIt's mad libs meets gangsta rap y'all.",
        parse_mode=ParseMode.HTML,
    )


def inlinequery(update: Update, context: CallbackContext) -> None:
    user_query = update.inline_query.query
    chat = gizoogle(user_query)
    if user_query == "":
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Gangsta",
            input_message_content=InputTextMessageContent(chat),
        )
    ]
    update.inline_query.answer(
        results=results,
        switch_pm_text="Type something !",
        switch_pm_parameter="sourcecode",
    )


# https://stackoverflow.com/questions/41636867/how-can-i-share-a-variable-between-functions-in-python
@send_action(ChatAction.TYPING)
def gangsta(update, context):
    user_message = update.message.text
    chat = gizoogle(user_message)
    update.message.reply_text(chat)


@send_action(ChatAction.UPLOAD_VOICE)
# TODO: Find any male tts module
# This is funny a male bot with female voice
def tts(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    argument = context.args
    user_says = " ".join(context.args)
    chat = gizoogle(user_says)
    if len(argument) == 0:
        update.message.reply_text(
            "Faggot, what did you expect a audio use /tts some text !."
        )
    else:
        tts = gTTS(chat)
        voicy = tts.save("snoopy.mp3")
        bot.send_audio(
            chat_id=chat_id, performer="snoopdog", audio=open("snoopy.mp3", "rb")
        )
        # removing the waste audio file
        os.remove("snoopy.mp3")


def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pg13", pg13))
    dp.add_handler(CommandHandler("tts", tts))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, gangsta))
    dp.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
