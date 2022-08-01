from const_vars import *
from cut_res_to_output import cut_res_to_output
import json
import glob
from mail_from_yahoo import mail_from_yahoo
import os
import smtplib
import time
import json
from deepdiff import DeepDiff
import telebot
from telebot import types

# dir_name = 'Data_darxtron/'
def create_res_msg(dir_name):
    list_of_files = list(glob.glob(dir_name + '*'))
    list_of_files.sort(key=lambda x: os.path.getmtime(x))

    with open(list_of_files[-1], 'r') as file:
        data = file.read()
        new_data = json.loads(data)

    with open(list_of_files[-2], 'r') as file:
        data = file.read()
        old_data = json.loads(data)

    res = DeepDiff(old_data, new_data)
    res_value = res['values_changed'] if res['values_changed'] else ['Нет изменений']

    old_file_time = time.ctime(os.path.getctime(list_of_files[-2]))
    new_file_time = time.ctime(os.path.getctime(list_of_files[-1]))
    print(str(list_of_files[-1]), str(list_of_files[-2]))

    cutting_res_list = cut_res_to_output(res_value)[-101:] if len(cut_res_to_output(res_value)) > 102 else cut_res_to_output(res_value)
    res_msg_data = f'Prices changed:\nSince {old_file_time}\nTill {new_file_time}\n\n'
    count_of_chng = len(cut_res_to_output(res_value))
    for i in cutting_res_list:
        add_str_value = f'{i[0]}   :   {i[1]}\n'
        res_msg_data += add_str_value
    res_msg_data += f'\nтут до 100 изменений, всего {count_of_chng}'
    res_msg_data += '\n\nGood Luck! )'
    return res_msg_data



def telegram_bot(token_tg):
    bot = telebot.TeleBot(token_tg)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('darxtron')
        btn2 = types.KeyboardButton('3ddiy')
        btn3 = types.KeyboardButton('cnc-tehnologi')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите магазин', parse_mode='html', reply_markup=markup)
    @bot.message_handler(content_types=['text'])
    def send_diff(message):
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        # btn1 = types.KeyboardButton('darxtron')
        # btn2 = types.KeyboardButton('3ddiy')
        # markup.add(btn1, btn2)
        # bot.send_message(message.chat.id, 'Выберите начальную дату', parse_mode='html', reply_markup=markup)

        if message.text.lower() == 'darxtron':
            dir_name = 'Datas/Data_darxtron/'
        elif message.text.lower() == '3ddiy':
            dir_name = 'Datas/Data_3ddiy/'
        elif message.text.lower() == 'cnc-tehnologi':
            dir_name = 'Datas/Data_cnc/'
        else:
            bot.send_message(message.chat.id, 'Нажмите кнопку магазина')
        try:
            bot.send_message(
            message.chat.id,
            create_res_msg(dir_name)
            )
        except KeyError as e:
            error_msg = 'no changes'
            bot.send_message(
            message.chat.id,
            error_msg
            )
        except Exception as e:
            print(e)
            error_msg = 'something goes wrong.. pls, try again later'
            bot.send_message(
            message.chat.id,
            error_msg
            )
    bot.polling()

telegram_bot(token_tg)

# if __name__ =='__main__':
#     create_res_msg('Data_3ddiy/')