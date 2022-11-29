import os
from flask import Flask,render_template,request,redirect
import time
import threading
import telebot


TOKEN = '5072766021:AAHN57wjgpEG1c6OSqoMeYXbRBdbeGgElYs'
bot = telebot.TeleBot(TOKEN)
#app=Flask(__name__)
server = Flask(__name__)

 
@bot.message_handler(commands=['start'])
def start(message):
  bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

def akhil():
  a=0
  while True:
    a+=1
    bot.send_message(chat_id="685472615",text=f"{a}. running🌜")
    time.sleep(10)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
 
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + 'alivebots' + '.onrender.com/' + f"{TOKEN}")
    return "!", 200

@server.route('/home')
def GetMuessageyu():
  return("running")

threading.Thread(target=akhil, name='run_server_time', daemon=True).start()

if __name__ == "__main__":
  #server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
  #server.run(debug=True,host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
  server.run(debug=True,host="0.0.0.0", port=int(os.environ.get('PORT', 1000)))

