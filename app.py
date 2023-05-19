import os
import logging
import telebot
import re
import sys
from telebot import types,util
from telebot import custom_filters
import time
import random
import traceback
from flask import Flask,render_template,request,redirect

from config import GENERALCHANNEL,PostText,AdText

from DetaDatabase import AddChannel,GetAllChannel,CheckAuthUser,UpdateTotalPost,GetLastPostId,UpdateAdTextMsgId,GetPostChannelId
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) 


API_TOKEN = '1921522398:AAFdwDnD-Odv5XdP7sxTosn3nRspkEnetZI'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

ValidDomain = [
  "terabox.com",
  "nephobox.com",
  "momerybox.com",
  "teraboxapp.com"
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

@bot.message_handler(commands=['random'])
def randomPosts(m):
  h = GetLastPostId()
  ChnlList = GetAllChannel()
  x = random.sample(range(2,int(h)), 10)
  yyy = 0
  for xt in x:
    for i in ChnlList:
      bot.forward_message(chat_id =i, from_chat_id = POSTCHANNEL, message_id = xt)
      time.sleep(2)
    yyy+=1
    bot.send_message(m.chat.id,f"{yyy}/10")
  #if m.chat.id in ChnlList:#try:
    #msg = bot.send_message(m.chat.id,AdText.format("https://t.me/+wtLFZQLoCuhiNDBl"),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
  #else:#except:
    #AddChannel(m.chat.id)
    #msg = bot.send_message(m.chat.id,AdText.format("https://t.me/+wtLFZQLoCuhiNDBl"),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
    
    
@bot.message_handler(commands=['fetch'])
def fetchresult(m):
  chnlList = GetAllChannel()
  ChatDetail = """
  Id = {}
  Name = {}
  Url = {}
  Subscribers = {}
  """
  for i in chnlList:
    try:
      chatdtl = bot.get_chat(f"{i}")
      chatId = chatdtl.id
      chatTtl = chatdtl.title
      chatUrl = chatdtl.invite_link
      Susb = bot.get_chat_members_count(f"{i}")
      bot.send_message(m.chat.id,ChatDetail.format(chatId,chatTtl,chatUrl,Susb))
    except Exception as e:
      bot.send_message(m.chat.id,f"id={i}\n\n{e}")
    


@bot.message_handler(func=lambda message:True,chat_id=[1023650988,1958848922], content_types=['photo'])
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
  
@bot.message_handler(func=lambda message:True, content_types=['photo'])
def Photonot(m):
  bot.send_message(m.chat.id,"Personal Bot")

@bot.channel_post_handler()
def Send_Post(m):
  h = GetLastPostId()
  ChnlList = GetAllChannel()
  for i in range(3):
    pstid = random.randint(2,int(h))
    bot.forward_message(chat_id = m.chat.id, from_chat_id = POSTCHANNEL, message_id = pstid)
    time.sleep(2)
  if m.chat.id in ChnlList:#try:
    msg = bot.send_message(m.chat.id,AdText.format("https://t.me/+RcRxo6Yt8kQ4MjA1"),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
  else:#except:
    AddChannel(m.chat.id)
    msg = bot.send_message(m.chat.id,AdText.format("https://t.me/+RcRxo6Yt8kQ4MjA1"),parse_mode="html")
    #UpdateAdTextMsgId(msg.id)
    

@bot.message_handler(content_types=["new_chat_members"])
def new_member(message: types.Message):
  try:
    # get new chat member
    #new_user_id = message.json.get("new_chat_member").get("id")
    #new_user = bot.get_chat_member(message.chat.id, new_user_id).user
    # Restrict new member
    h = GetLastPostId()
    #ChnlList = GetAllChannel()
    #for i in range(3):
    pstid = random.randint(2,int(h))
    bot.forward_message(chat_id = message.chat.id, from_chat_id = POSTCHANNEL, message_id = pstid)
    #time.sleep(2)
  except Exception as e:
    Yyy = traceback.format_exc()
    bot.send_message(chat_id=699412278,text=Yyy)
  
bot.add_custom_filter(custom_filters.ChatFilter())
    

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
 
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://tera2nd-solo.onrender.com/' + f"{API_TOKEN}")
    return "!uk", 200
 
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 1000)))
#bot.infinity_polling() 
