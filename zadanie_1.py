import logging
import os
import re
from datetime import datetime
import time
import socket
import librosa
import psycopg2
from tinkoff_voicekit_client import ClientSTT

#Подключаемся к тинькоф библиотеке
API_KEY = "Введите свой ключ"
SECRET_KEY = "Введите свой ключ"

client = ClientSTT(API_KEY, SECRET_KEY)

audio_config = {
    "encoding": "LINEAR16",
    "sample_rate_hertz": 8000,
    "num_channels": 1
}

#Принимаем информацию из консоли. 
print('Приветствую, укажите путь к файлу .wav в формате C:/Files/audiofile.wav')
pat_h = input()
if pat_h.split('.')[-1] != 'wav':
    print( 'Файл должен быть формата .wav!')
    exit()
else:
    print('good')
print('Укажите номер телефона')
phone_number = input()
print('Нужно ли делать запись в базу данных?')
choice_db = input()
if choice_db == "да":
    go_bd = True
else:
    go_bd = False

#Распознаем слова из аудио
response = client.recognize(pat_h, audio_config)

del response[1:]
droblenie_1 = response[0].pop('alternatives')
droblenie_2 = droblenie_1[0]
result = droblenie_2.pop('transcript')
print(result)

# Делаем из строк со словами - список со словами + задаем слова на распознавание автоответчика и положительной/отрицательной реакции
wordList = re.sub("[^\w]", " ",  result).split()

avtoWords = ['автоответчик', 'авто', 'ответчик', 'сообщение', 'после', 'оставьте' 'сигнала', 'вас', 'приветствует']
yesWords = ['да', 'конечно', 'давай', 'давайте', 'йес', 'cогласен', 'недолго', 'долго', 'говорите', 'немного', 'ладно', 'хорошо', 'слушаю']
noWords = ['нет','неудобно','отказываюсь','отказ','занят','не','против','ноу']


#Проверяем на автоответчик
for word3 in avtoWords:
    if word3 in wordList:
        etap_1 = 0
        who_is = 'AO'
    else:
        etap_1 = 1
        who_is = 'Human'
print(etap_1)
#Проверяем на положительный/отрицательный ответ
if etap_1 == 1:
    for word1 in yesWords:
        if word1 in wordList:
            etap_2 = 1

    for word2 in noWords:
        if word2 in wordList:
            etap_2 = 0
else:
    etap_2 = '-'
    print('Второго этапа не будет')    

#Фиксируем дату и время
date_time = str(datetime.now())

date_spliter = date_time.split(' ')
time_spliter = date_spliter[1].split('.')

date = date_spliter[0]
time = time_spliter[0]

#Узнаем id результата распознавания и длительность аудио
unique_id = id(result)
duration = librosa.get_duration(filename=pat_h)


#Таблица project
test = 'Testing'
description_1 = '-'

#Узнаем имя хоста и ip. Таблица server
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
description_2 = '-'

#Создаем лог-файл и фиксируем в него инфу
logging.basicConfig(level = logging.DEBUG, filename = "tinkoff.log")
logging.debug('Logging: %s', {'date':date, 'time':time, 'unique_id':unique_id, 'who_is' : who_is, 'etap_2': etap_2, 'phone_number':phone_number, 'duration':duration, 'result':result})

#Подключаемся к БД(сделанную через pgAdmin), вносим данные (в т.ч. Foreign Key), отлавлиаем ошибки и пишем их в отдельный лог-файл

if go_bd == True:
    connection = psycopg2.connect(dbname="x-lab_voice", user="postgres", password="faqser95", host="localhost", port='5432')

    try:
        cursor = connection.cursor()

        voice_data_insert_query = """ INSERT INTO voice_data (date, time, unique_id, who_is, etap_2, phone_number, duration, result) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (date, time, unique_id, who_is, etap_2, phone_number, duration, result)
        cursor.execute(voice_data_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount    
        print (count, "Информация загружена в Базу Данных")

        project_insert_query = """ INSERT INTO fk_project (name_1, description_1) VALUES (%s,%s)"""
        record_to_insert_2 = (test, description_1)
        cursor.execute(project_insert_query, record_to_insert_2)

        server_insert_query = """ INSERT INTO fk_server (hostname, ip_address,description_2) VALUES (%s,%s,%s)"""
        record_to_insert_3 = (hostname, ip_address, description_2)
        cursor.execute(server_insert_query, record_to_insert_3)


        connection.commit()
    except (Exception, psycopg2.Error) as error :
        if(connection):
            logging.basicConfig(level = logging.DEBUG, filename = "errors.log")
            logging.debug('Catching errors: %s', {'error' : error})
            print("Не получилось сделать запись в БД", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("Закрываем соединение с БД")
else:
    print('Человек или АО:', who_is, 'Результат второго этапа:', etap_2)
#Удаляем файл
os.remove(pat_h)

