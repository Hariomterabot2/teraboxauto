#import logging
import os
#from config import Config
#import pyrogram
#from pyrogram import Client
from config import AuthUser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
 
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger(__name__)
#logging.getLogger("pyrogram").setLevel(logging.WARNING)
 
 
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("herotelebot.json", scope)
client = gspread.authorize(creds)
ak = client.open("Manishforward ")
general = ak.worksheet("general")
channels = ak.worksheet("channels")

def CheckAuthUser(UserId):
    if int(UserId) in AuthUser:
        return True
    else:
        None
        
def AddChannel(ChnlId):
  cells = channels.findall(str(ChnlId))
  if len(cells) > 0:
    return True
  else:
    h = channels.get('A51').first()
    h1 = int(h) + 1
    channels.update_cell(int(h1),1 ,f"{h1}")
    channels.update_cell(int(h1),2 ,ChnlId)
    
def GetAllChannel():
    values_list = channels.col_values(2)
    return values_list
    
def UpdateTotalPost(msgid):
    general.update("B1",msgid)
    
def GetLastPostId():
    h = general.get('B1').first()
    return h
    
def UpdateAdTextMsgId(ID):
    print("123")

def GetPostChannelId():
    Id = "-100" + str(general.get("B2").first())
    return int(Id)
