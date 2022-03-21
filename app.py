from flask import Flask, render_template, request, redirect
from decouple import config
import telebot
import mysql.connector
import os

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="telebot"
)

app = Flask(__name__)

bot = telebot.TeleBot('5155236337:AAFYLqTq3unfn65R1MX_AtagaW0tDTU1Ito')


@app.route("/")
def index():
    cursorObjectForFetch = dataBase.cursor(dictionary=True)
    query = "SELECT * FROM message"
    cursorObjectForFetch.execute(query)
    botMessages = cursorObjectForFetch.fetchall()
    # dataBase.close()
    return render_template('index.html', botMessages=botMessages)


@app.route("/addMessage")
def addMessage():
    return render_template('addMessage.html')


@app.route('/save', methods=['POST'])
def save():
    cursorObjectForInsert = dataBase.cursor()
    botCommand = request.form['botCommand']
    botMessage = request.form['botMessage']
    print(botMessage)

    sql = "INSERT INTO message (command, message) VALUES (%s, %s)"
    val = (botCommand, botMessage)
    cursorObjectForInsert.execute(sql, val)
    dataBase.commit()
    # dataBase.close()

    return redirect("/")


@app.route('/edit', methods=['GET'])
def edit():
    cursorObjectForFetch = dataBase.cursor(dictionary=True)
    edit_id = request.args['id']

    sql = "SELECT * FROM message WHERE id=" + edit_id
    cursorObjectForFetch.execute(sql)
    botMessage = cursorObjectForFetch.fetchall()

    return render_template('editMessage.html', botMessage=botMessage[0])


@app.route('/delete', methods=['GET'])
def delete():
    cursorObjectForFetch = dataBase.cursor(dictionary=True)
    edit_id = request.args['id']
    print(edit_id)
    sql = "DELETE FROM message WHERE id=" + edit_id
    cursorObjectForFetch.execute(sql)
    dataBase.commit()

    return redirect("/")


@app.route('/update', methods=['POST'])
def update():
    cursorObjectForInsert = dataBase.cursor()
    botCommand = request.form['botCommand']
    botMessage = request.form['botMessage']
    edit_id = request.form['id']

    sql = "UPDATE message SET command = %s, message = %s WHERE id=" + edit_id
    val = (botCommand, botMessage)
    cursorObjectForInsert.execute(sql, val)
    dataBase.commit()
    # dataBase.close()

    return redirect("/")


@app.route('/setting', methods=['GET'])
def setting():
    cursorObjectForFetch = dataBase.cursor(dictionary=True)

    sql = "SELECT * FROM settings"
    cursorObjectForFetch.execute(sql)
    setting = cursorObjectForFetch.fetchall()

    return render_template('setting.html', setting=setting[0])


@app.route('/update_setting', methods=['POST'])
def update_setting():
    cursorObjectForInsert = dataBase.cursor()
    app_id = request.form['app_id']
    api_hash = request.form['api_hash']
    bot_token = request.form['bot_token']
    phone = request.form['phone']
    channel_name = request.form['channel_name']
    group_name = request.form['group_name']

    sql = "UPDATE settings SET API_ID = %s, API_HASH = %s, BOT_TOKEN = %s, PHONE = %s, CHANNEL_NAME = %s, GROUP_NAME = %s  WHERE id = 1"
    val = (app_id, api_hash, bot_token, phone, channel_name, group_name)
    cursorObjectForInsert.execute(sql, val)
    dataBase.commit()

    return redirect("/setting")

# @app.route('/update-env', methods=['GET'])
# def update_env():
#     with open("../.env", "r") as f:
#         for line in f.readlines():
#             try:
#                 key, value = line.split('=')
#                 os.putenv(key, value)
#                 print(key)
#                 print(value)
#             except ValueError:
#                 # syntax error
#                 pass
#     file = open(r'../.env', 'r').read()
#     with open("../.env", "w") as f:
#         f.write("username=John /n")
#         f.write("email=abc@gmail.com")
#     return exec(file)
#     return "abc"


# @app.route('/run-script', methods=['GET'])
# def run_script():
#    result = subprocess.check_output("python Telebot/botReply.py", shell=True)
#    return render_template('results.html', **locals())
