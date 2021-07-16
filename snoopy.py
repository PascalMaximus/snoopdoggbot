import logging
import os
import re
import argparse
import bs4
import requests
from gtts import gTTS
from urllib import parse
from uuid import uuid4
# importing everything from ptb (im lazy af to list all things) maybe later
from telegram import *
from telegram.ext import *
from telegram.utils.helpers import *


# basic logging stuff in case something goes wrong
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
            InlineKeyboardButton("Join Mah Channel", url= "https://telegram.dog/botivity")
        ]
  
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Yo whatsup {user.mention_markdown_v2()} rap wit me or i will kick you read /pg13 before using please and join ma channel  @botivity\!', reply_markup=reply_markup)
    
# In case snoopdogg goes too much rogue (just a precaution also this is copied from gizoogle.net you can find it there minor modifications are made though)    
def pg13(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(" <u>Some Obscene Language</u> \n\nThis bot is only intended for mature audiences farmiliar with the gangsta slang used by Snoop Dogg, and anybody under the age of 13 should not even think about using this bot without adult supervision.\nApologies if you are in any way offended by the explicit wording used in the translations.\nThe slanguage used in our algorithm has been quoted from Snoop Dogg himself and is commonly used in movies, conversations and music he has written.\nThese words are based on slang and can not be interpreted in any other way other than how they are quoted. There are no racist words used in the algorithm.\nIt's mad libs meets gangsta rap y'all.", parse_mode=ParseMode.HTML)

#  Decorator for chat actions such as sending a message , sending a photo , sending a audio , sending a video etc. etc. you can find all the methods in python telegram bot documentation    
from functools import wraps
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context,  *args, **kwargs)
        return command_func
    return decorator

# TODO: Modularize code and prevent repeatation 
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
  try:
      bot.send_audio(chat_id=chat_id, performer="snoopdog",audio=open('snoopy.mp3', 'rb'))
  except Exception as e:
      update.message.reply_text("Faggot, What did you expect a voice ,Needs an argument, for eg:/tts i am a stupid guy who don't know to use a tts command ")

  else:
      update.message.reply_text("Faggot, What did you expect a voice ,Needs an argument, for eg:/tts i am a stupid guy who don't know to use a tts command ")
    
  finally:
      os.remove


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
if __name__ == '__main__':
    main()