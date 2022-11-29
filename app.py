import os
from flask import Flask,render_template,request,redirect
import time

server = Flask(__name__)

while True:
  print("akhil")
  print("kyu")
  time.sleep(10)



@server.route('/')
def getMessage():
  return("running")

if __name__ == "__main__":
  #threading.Thread(target=runAutoList, name='run_server_time', daemon=True).start()
  #server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
  #server.run(debug=True,host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
  server.run(debug=True,host="0.0.0.0", port=int(os.environ.get('PORT', 1000)))

