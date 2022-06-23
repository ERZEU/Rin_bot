import telebot
from telebot import types

token = open('C:/Secret/token_Rin_bot.txt','r')

bot = telebot.TeleBot(token.read())
calendar = []
id_Dev = 481892408
id_Kara = 366447369 #tg-Карина

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Записаться")
    btn2 = types.KeyboardButton("Задать вопрос")
    markup.add(btn1, btn2)

    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>. ' \
           f'Меня зовут Рин, я помогу тебе записаться на прием!' \

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    bot.send_message(message.chat.id, message.from_user)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Записаться"):
        temp = bot.send_message(message.chat.id, text="Напиши дату и время встречи в формате \nдд.мм.гг чч:мм (21.05.2022 13:59)")
        bot.send_message(message.chat.id, 'Существующие записи: ' + str(calendar))
        bot.register_next_step_handler(temp, create_entry)

    elif(message.text == "Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn1 = types.KeyboardButton("Получить контакты администратора")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, back)
        temp3 = bot.send_message(message.chat.id, text="Задай мне вопрос в виде обычного сообщения...", reply_markup=markup)
        bot.register_next_step_handler(temp3, asker)

    elif (message.text == "Получить контакты администратора"):
        bot.send_message(message.chat.id, "@siera_lis")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Записаться")
        button2 = types.KeyboardButton("Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

def create_entry(message):
    if(message.text == 'Задать вопрос' or message.text == 'Записаться'):
        func(message)

    elif (calendar.count(message.text) == 0):
        calendar.append(message.text)
        bot.send_message(message.chat.id, 'Запись создана!\n Ждем вас  ' + message.text)
        sen = 'Зай, новая запись!\n' + message.from_user.first_name + ' ' + message.from_user.last_name + ' ' + message.text
        bot.send_message(id_Kara, sen)

        print(calendar)
    elif(calendar.count(message.text) > 0):
        temp2 = bot.send_message(message.chat.id, 'На это время уже есть запись.\nВведите другую дату и время:')
        bot.register_next_step_handler(temp2, create_entry)

def asker(message):
    if(message.text != 'Получить контакты администратора' and message.text != 'Вернуться в главное меню' ):
        sen_ask = 'Зай, тут вопрос от ' + '@' + message.from_user.username + '\n' + '"' + message.text + '"'
        bot.send_message(id_Kara, sen_ask)
        bot.send_message(message.chat.id, 'Я передала ваш вопрос администратору, ожидайте ответа...')
    else:
        func(message)

bot.polling(none_stop=True)
