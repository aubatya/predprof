from app.service import *
import telebot
import time
import datetime as dt
from time import sleep
from datetime import date
from datetime import timedelta

import PIL
import sqlite3
from PIL import Image, ImageDraw
token = '5344136923:AAGF0VEGH66s5SJV2Q_eMBSuPkvJsX4Gx1E'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])


def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Маршрут','Карта')
    keyboard.row('Добавить датчик')
    bot.send_message(message.chat.id,"Добрый день, сталкер.")
    bot.send_message(message.chat.id,"Вы можете построить безопасный маршрут с помощью кнопки 'маршрут'")
    bot.send_message(message.chat.id,"Вы можете ввести актуальные данные с помощью кнопки 'ввод данных'")
    send = bot.send_message(message.chat.id,"Вы можете посмотреть карту анамалий с помощью кнопки 'карта' ",reply_markup = keyboard)
    
    bot.register_next_step_handler(send,main_menu)
        
@bot.message_handler(func=lambda message: True)

def main_menu(message):
    if message.text == 'Маршрут':
        find_coords(message)
    if message.text == 'Карта':
        build_map(message)
    if message.text == 'Добавить датчик':
        adding(message)
    

    if message.text == 'Главное меню':
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Маршрут','Карта')
        keyboard.row('Ввод данных')
        bot.send_message(message.chat.id,"Добрый день, сталкер.")
        bot.send_message(message.chat.id,"Вы можете построить безопасный маршрут с помощью кнопки 'маршрут'")
        bot.send_message(message.chat.id,"Вы можете ввести актуальные данные с помощью кнопки 'ввод данных'")
        send = bot.send_message(message.chat.id,"Вы можете посмотреть карту анамалий с помощью кнопки 'карта' ",reply_markup = keyboard)
        bot.register_next_step_handler(send,main_menu)
def adding(message):
    send = bot.send_message(message.chat.id,"Введите ID датчика и его координаты через пробел (ID x y)")
    bot.register_next_step_handler(send,new_adding)
def new_adding(message):
    mas = (message.text).split()
    if len(mas)<3:
        send = bot.send_message(message.chat.id,'Ошибка! Неверный ввод данных')
        adding(message)
    else:
        send = bot.send_message(message.chat.id,'Введите кол-во аномалий на координате')
#        bot.register_next_step_handler(send,amount_anomaly,mas)   
#def amoun_anomaly(message,mas):
  #  for i in range(int(message.text)):
  #      adding_new_values([mas,[
def find_coords(message):
    send = bot.send_message(message.chat.id,"Введи координаты начала и конца маршрута через пробел (x1 y1 x2 y2)")
    bot.register_next_step_handler(send,drow_way)

def drow_way(message):
    mas = (message.text).split()
    if len(mas)<4:
        send = bot.send_message(message.chat.id,'Ошибка! Координаты введены неверно')
        find_coords(message)
    else:
        x1,y1,x2,y2 = map(int,(message.text).split())
        m = build_way((x1,y1),(x2,y2))
        keyboard = telebot.types.ReplyKeyboardMarkup()
        keyboard.row('Главное меню')
        im = Image.open('map1.png')
        draw = ImageDraw.Draw(im)
        for i in range(len(m)-1):
            draw.line((m[i][0]*50, m[i][1]*50, m[i+1][0]*50, m[i+1][1]*50), fill="red", width=5)
        im.save("map2.png")
        img = open('map2.png','rb')
        bot.send_photo(message.chat.id,img)
        send = bot.send_message(message.chat.id,'Самый безопасный маршрут',reply_markup = keyboard)
        bot.register_next_step_handler(send,main_menu)    

def build_map(message):
    #m = build_anamaly_map()
    m = [[1,1], [4, 4], [10, 3], [3, 15]]

    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Главное меню')
    im = Image.open('map.png')
    draw = ImageDraw.Draw(im)
    for i in range(len(m)):
        draw.ellipse([m[i][0]*50-8, m[i][1]*50-8, m[i][0]*50+8, m[i][1]*50+8], fill="red")
    im.save("map1.png")
    
    img = open('map1.png','rb')
    bot.send_photo(message.chat.id,img)
    send = bot.send_message(message.chat.id,"Актуальная карта аномалий",reply_markup = keyboard)
    bot.register_next_step_handler(send,main_menu)

bot.polling(none_stop=False,interval=1)

