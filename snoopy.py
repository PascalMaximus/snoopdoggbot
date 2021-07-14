import logging
from telegram import *
from telegram.ext import *
from telegram.utils.helpers import *
from gtts import gTTS
import re
import bs4
from urllib import parse
import requests
import argparse
from uuid import uuid4
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "")
bot = Bot(TOKEN)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Use me inline 🐾 ", switch_inline_query_current_chat =""),
            InlineKeyboardButton("Mah Channel", url= "https://telegram.dog/botivity")
        ]
  
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Yo whatsup {user.mention_markdown_v2()} rap wit me or i will kick you read /pg13 before using please and join ma channel  @botivity\!', reply_markup=reply_markup)
    
    
def pg13(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(" <u>Some Obscene Language</u> \n\nThis bot is only intended for mature audiences farmiliar with the gangsta slang used by Snoop Dogg, and anybody under the age of 13 should not even think about using this bot without adult supervision.\nApologies if you are in any way offended by the explicit wording used in the translations.\nThe slanguage used in our algorithm has been quoted from Snoop Dogg himself and is commonly used in movies, conversations and music he has written.\nThese words are based on slang and can not be interpreted in any other way other than how they are quoted. There are no racist words used in the algorithm.\nIt's mad libs meets gangsta rap y'all.", parse_mode=ParseMode.HTML)
    
from functools import wraps
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator
    

def inlinequery(update: Update, context: CallbackContext) -> None:
  
    query = update.inline_query.query
    params = {"translatetext": query}
    target_url = "http://www.gizoogle.net/textilizer.php"
    resp = requests.post(target_url, data=params)
    soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
    soup = bs4.BeautifulSoup(soup_input, "lxml")
    giz = soup.find_all(text=True)
    giz_text = giz[37].strip("\r\n")
  
    if query == "":
        return

  
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Gangsta",
            input_message_content=InputTextMessageContent(
                f"{escape_markdown(giz_text)}"
            ),
            )
    ]

    update.inline_query.answer(results=results,
    switch_pm_text='search something!',
    switch_pm_parameter='inline-help',
    cache_time=0,
    auto_pagination=True,)

@send_action(ChatAction.TYPING)
def gangsta(update, context):
  input_text = update.message.text
  params = {"translatetext": input_text}
  target_url = "http://www.gizoogle.net/textilizer.php"
  resp = requests.post(target_url, data=params)
  soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
  soup = bs4.BeautifulSoup(soup_input, "lxml")
  giz = soup.find_all(text=True)
  giz_text = giz[37].strip("\r\n")
  update.message.reply_text(giz_text)
  
@send_action(ChatAction.UPLOAD_VOICE)
def tts(update: Update, context: CallbackContext) -> None:
  chat_id = update.effective_chat.id
  user_says = " ".join(context.args)
  params = {"translatetext": user_says}
  target_url = "http://www.gizoogle.net/textilizer.php"
  resp = requests.post(target_url, data=params)
  soup_input = re.sub("/name=translatetext[^>]*>/", 'name="translatetext" >', resp.text)
  soup = bs4.BeautifulSoup(soup_input, "lxml")
  giz = soup.find_all(text=True)
  giz_text = giz[37].strip("\r\n")
  tts = gTTS(giz_text)
  voicy = tts.save('snoopy.mp3')
  if voicy:
      bot.send_audio(chat_id=chat_id, performer="snoopdog",audio=open('snoopy.mp3', 'rb'))
  else update.message.reply_text("Faggot, Needs an argument, for eg:/tts i am a stupid guy who don't know to use a tts command ")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("pg13", pg13))
    dispatcher.add_handler(CommandHandler("tts", tts))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, gangsta))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
