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

group_name = getSettings[0]['GROUP_NAME']
api_id = getSettings[0]['API_ID']        # YOUR API_ID
api_hash = getSettings[0]['API_HASH']       # YOUR API_HASH
phone = getSettings[0]['PHONE']    # YOUR PHONE NUMBER, INCLUDING COUNTRY CODE
client = TelegramClient(phone, api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


def add_users_to_group():
    # input_file = sys.argv[1]
    input_file = sys.argv[1] if len(sys.argv) > 1 else '.'
    users = []
    with open(input_file+ '/members-test-video-channel.csv', encoding='UTF-8') as f:
        rows = csv.reader(f,delimiter=",",lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            try:
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
            except IndexError:
                print ('users without id or access_hash')
            users.append(user)

    #random.shuffle(users)
    chats = []
    last_date = None
    chunk_size = 10
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
            if chat.megagroup== True: # CONDITION TO ONLY LIST MEGA GROUPS.
                groups.append(chat)
        except:
            continue

    print('Choose a group to add members:')
    i=0
    for group in groups:
        # print(str(i) + '- ' + group.title)
        if(group.title == group_name):
            g_index = i
        i+=1

    # g_index = input("Enter a Number: ")
    target_group=groups[int(g_index)]
    print('\n\nGrupo elegido:\t' + groups[int(g_index)].title)

    target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

    # mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
    mode = 2

    error_count = 0

    for user in users:
        try:
            print ("Adding {}".format(user['username']))
            if mode == 1:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(target_group_entity,[user_to_add]))
            print("Waiting 30 Seconds...")
            time.sleep(30)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            error_count += 1
            if error_count > 10:
                sys.exit('too many errors')
            continue


add_users_to_group()
