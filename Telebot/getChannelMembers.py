from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from decouple import config
import sys
import csv
import traceback
import time
import random
import re
import mysql.connector


dataBase = mysql.connector.connect(
    host ="localhost",
    user ="root",
    passwd ="",
    database = "telebot"
)
cursorObject = dataBase.cursor(dictionary=True)

queryForGetSettings = "SELECT * FROM settings"
cursorObject.execute(queryForGetSettings)

getSettings = cursorObject.fetchall()

channel_name = getSettings[0]['CHANNEL_NAME']
api_id = getSettings[0]['API_ID']        # YOUR API_ID
api_hash = getSettings[0]['API_HASH']       # YOUR API_HASH
phone = getSettings[0]['PHONE']    # YOUR PHONE NUMBER, INCLUDING COUNTRY CODE
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


def list_users_in_group():
    chats = []
    last_date = None
    chunk_size = 200
    groups=[]
    
    result = client(GetDialogsRequest(
                offset_date=last_date,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=chunk_size,
                hash = 0
            ))
    chats.extend(result.chats)
    
    for chat in chats:
        try:
            print(chat)
            groups.append(chat)
            # if chat.megagroup== True:
        except:
            continue
    
    print('Choose a group to scrape members from:')
    i=0
    for g in groups:
        # print(str(i) + '- ' + g.title)
        if(g.title == channel_name):
            g_index = i
        i+=1

    
    # g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]

    print('\n\nGrupo elegido:\t' + groups[int(g_index)].title)
    
    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=True)
    
    print('Saving In file...')
    with open("members-" + re.sub("-+","-",re.sub("[^a-zA-Z]","-",str.lower(target_group.title))) + ".csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print('Members scraped successfully.')


list_users_in_group()
