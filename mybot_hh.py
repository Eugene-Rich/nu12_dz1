import telebot
from api_hh02 import getvkans

TOKEN = '7077603584:AAEoaSsY6cArOZ2IiL1chVT81zOmiInxco0'

bot = telebot.TeleBot(TOKEN)

kash = {} # Словарь для хранения кэша запросов

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Для начала работы бота введите команду \n /vac <Наименование вакансии>,<Город>.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Для начала работы бота введите команду \n /vac <Наименование вакансии>,<Город>.")

@bot.message_handler(commands=['vac'])
def send_help(message):
    prm = ' '.join(message.text.split(' ')[1:])

    lstvac = kash.get(prm)
    if lstvac == None: # Не нашли такой запрос в кэше. Будем формировать запрос и выполнять его.
        if prm == '':
            bot.reply_to(message, 'Укажите параметры <Наименование вакансии>,<Город>')
        else:
            # Получим параметры запроса из команды
            naimvac = prm.split(',')[0]
            gorod = prm.split(',')[1]
            bot.reply_to(message, 'Запрашиваются данные по вакансии' + '\n' + naimvac + ' ' '\n' + 'В городе '+ gorod)

            # Получим данные из HH
            lstvac = getvkans(naimvac, gorod)

            # Сохраним в кэше запрос и ответ на него
            kash[prm] = lstvac # Сохраним в кэше запрос и ответ на него
    else:
        bot.reply_to(message, 'Данные выданы из кэша ' + prm)

   # Выведем в бот ответ пользователю.
    for ls in lstvac:
         bot.reply_to(message, str(ls[0])  + '\n' + str(ls[1]))

bot.polling()
