import os
from flask import Flask,render_template,request,redirect
import telebot



TOKEN = '2109918986:AAEJ1kY-YvP0pKkG_5n1bmF_VPiYJ5lQ98I'
bot = telebot.TeleBot(TOKEN)
#app=Flask(__name__)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
 
@server.route("/")
def webhook():
    bot.remove_webhook()
    #bot.set_webhook(url='https://deshiapp.herokuapp.com/' + f"{TOKEN}")
    bot.set_webhook(url='https://deshi-app-meenaakhlesh786.koyeb.com/' + f"{TOKEN}")
    return "!", 200
 
if __name__ == "__main__":
  #threading.Thread(target=runAutoList, name='run_server_time', daemon=True).start()
  #server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
  server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
 

#if __name__=='__main__':
    #app.run(debug=True)
