from decouple import config
import telebot
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
bot = telebot.TeleBot(getSettings[0]['BOT_TOKEN'])

# for command in botMessages:
@bot.message_handler(content_types=['text'])
def greet(message): 
    
    dataBase = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="",
        database = "telebot"
    )
    cursorObject = dataBase.cursor(dictionary=True)
    query = "SELECT * FROM message"
    cursorObject.execute(query)
    botMessages = cursorObject.fetchall()
    # print(botMessages)

    print(message.text[1:])
    for command in botMessages:
        if(command['command'] == message.text[1:] ):
            bot.reply_to(message, command['message'])
            



bot.infinity_polling()



