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

def create_res_msg(dir_name, since_time):
    list_of_files = list(glob.glob(dir_name + '*'))
    list_of_files.sort(key=lambda x: os.path.getmtime(x))

    with open(list_of_files[-1], 'r') as file:
        data = file.read()
        new_data = json.loads(data)

    if since_time == 'pairdays':
        i = -2
    elif since_time == 'week':
        i = -3
    elif since_time =='month':
        i = -4

    with open(list_of_files[i], 'r') as file:
        data = file.read()
        old_data = json.loads(data)

    res = DeepDiff(old_data, new_data)
    res_value = res['values_changed'] if res['values_changed'] else ['Нет изменений']

    old_file_time = time.ctime(os.path.getctime(list_of_files[i]))
    new_file_time = time.ctime(os.path.getctime(list_of_files[-1]))
    # print(str(list_of_files[-1]), str(list_of_files[-2]))

    cutting_res_list = cut_res_to_output(res_value)[-101:] if len(cut_res_to_output(res_value)) > 102 else cut_res_to_output(res_value)
    res_msg_data = f'Изменения цен:\nС {old_file_time}\nПо {new_file_time}\n\n'
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
           
        def send_final_msg():
            try:
                bot.send_message(
                message.chat.id,
                create_res_msg(dir_name, since_time)
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

        if message.text.lower() == 'darxtron':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('день')
            btn2 = types.KeyboardButton('неделя')
            btn3 = types.KeyboardButton('месяц')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите начальную дату', parse_mode='html', reply_markup=markup)

        elif message.text.lower() == 'день':
            since_time = 'pairdays'
            dir_name = 'Datas/Data_darxtron/'
            send_final_msg()
        elif message.text.lower() == 'неделя':
            since_time = 'week'
            dir_name = 'Datas/Data_darxtron/'
            send_final_msg()
        elif message.text.lower() == 'месяц':
            since_time = 'month'
            dir_name = 'Datas/Data_darxtron/'
            send_final_msg()
            
        elif message.text.lower() == '3ddiy':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('день.')
            btn2 = types.KeyboardButton('неделя.')
            btn3 = types.KeyboardButton('месяц.')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите начальную дату', parse_mode='html', reply_markup=markup)

        elif message.text.lower() == 'день.':
            since_time = 'pairdays'
            dir_name = 'Datas/Data_3ddiy/'
            send_final_msg()
        elif message.text.lower() == 'неделя.':
            since_time = 'week'
            dir_name = 'Datas/Data_3ddiy/'
            send_final_msg()
        elif message.text.lower() == 'месяц.':
            since_time = 'month'
            dir_name = 'Datas/Data_3ddiy/'
            send_final_msg()

        elif message.text.lower() == 'cnc-tehnologi':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('.день')
            btn2 = types.KeyboardButton('.неделя')
            btn3 = types.KeyboardButton('.месяц')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id, 'Выберите начальную дату', parse_mode='html', reply_markup=markup)
            
        elif message.text.lower() == '.день':
            since_time = 'pairdays'
            dir_name = 'Datas/Data_cnc/'
            send_final_msg()
        elif message.text.lower() == '.неделя':
            since_time = 'week'
            dir_name = 'Datas/Data_cnc/'
            send_final_msg()
        elif message.text.lower() == '.месяц':
            since_time = 'month'
            dir_name = 'Datas/Data_cnc/'
            send_final_msg()

        else:
            bot.send_message(message.chat.id, 'Нажмите кнопку магазина')
        
    bot.polling(none_stop=True)

telegram_bot(token_tg)

# if __name__ =='__main__':
