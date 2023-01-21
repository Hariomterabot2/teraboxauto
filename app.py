import os
import logging
import telebot
import re
import sys
from telebot import types,util
import time
import random
import traceback
from flask import Flask,render_template,request,redirect

from config import GENERALCHANNEL,PostText,AdText

from DetaDatabase import AddChannel,GetAllChannel,CheckAuthUser,UpdateTotalPost,GetLastPostId,UpdateAdTextMsgId,GetPostChannelId
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 


API_TOKEN = '5601716992:AAHm0pSfHH3ADojOovPDHlteaCXSBF8Buuo'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

ValidDomain = [
  "terabox.com",
  "nephobox.com",
  "momerybox.com"
  ]
  
POSTCHANNEL = GetPostChannelId()

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(m):
  if CheckAuthUser(m.chat.id) == True:
    bot.reply_to(m,"Runnung..")
  else:
    bot.reply_to(m,"you are not authrise")
  
@bot.message_handler(commands=['add'])
def add_channels(m):
    tt = util.extract_arguments(m.text)
    ListChnl = tt.split("\n")
    for i in ListChnl:
      Integer = isinstance(i, int)
      if Integer == True:
        xx = AddChannel(i)
        if xx == True:
          bot.reply_to(m,f"{i} Already In Database")
          time.sleep(1)
        else:
          bot.reply_to(m,f"Added {i}")
          time.sleep(2)
      else:
          bot.reply_to(m,f"Invalid {i}")
    
@bot.message_handler(commands=['fetch'])
def fetchresult(m):
    chnlList = GetAllChannel()
    


@bot.message_handler(func=lambda message:True, content_types=['photo'])
def command_default(m):
  photo_id = m.photo[-1].file_id
  OcaptionTitle = m.caption.split("\n")[0]
  TeraUrl = ""
  try:
    match = re.findall(r'(https?://[^\s]+)', f"{m.caption}")
    for url in match:
      data = url.split("/")[2]
      if str(data) in ValidDomain:
      #if (str(data) == "terabox.com" or str(data) == "nephobox.com"):
        TeraUrl+=url
        break
      else:
        continue
  except Exception as e:
    print(e)
  keyboard = types.InlineKeyboardMarkup()
  btn3 = types.InlineKeyboardButton(text=" ❤️Watch Online ", url=GENERALCHANNEL)
  keyboard.add(btn3)
  FData = PostText.format(OcaptionTitle,TeraUrl,TeraUrl,GENERALCHANNEL)
  msgy = bot.send_photo(chat_id=int(POSTCHANNEL),photo=photo_id,caption=FData,reply_markup=keyboard,parse_mode="html")
  try:
    UpdateTotalPost(msgy.id)
    ChnlList = GetAllChannel()
    #bot.send_message(m.chat.id,ChnlList)
    for vii in ChnlList:
      try:
        bot.send_photo(chat_id=int(vii),photo=photo_id,caption=FData,reply_markup=keyboard,parse_mode="html")
      except Exception as e:
        bot.send_message(m.chat.id,f"rr {e}")
        pass
    bot.reply_to(m,"Done❤️")
    time.sleep(2)
  except Exception as e:
    Xxx = sys.exc_info()
    Yyy = traceback.format_exc()
    bot.send_message(m.chat.id,Xxx)
    bot.send_message(m.chat.id,Yyy)
  
@bot.channel_post_handler()
def Send_Post(m):
  h = GetLastPostId()
  for i in range(3):
    pstid = random.randint(2,int(h))
    bot.forward_message(chat_id = m.chat.id, from_chat_id = POSTCHANNEL, message_id = pstid)
    time.sleep(2)
  try:
    msg = bot.send_message(m.chat.id,AdText.format(GENERALCHANNEL),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
  except:
    AddChannel(m.chat.id)
    msg = bot.send_message(m.chat.id,AdText.format(GENERALCHANNEL),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
    

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
 
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ManishTera.onrender.com/' + f"{API_TOKEN}")
    return "!", 200
 
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 1000)))
#bot.infinity_polling() 
