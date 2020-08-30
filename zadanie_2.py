from zadanie_1 import *

connection = psycopg2.connect(dbname="x-lab_voice", user="postgres", password="faqser95", host="localhost", port='5432')
cursor = connection.cursor()

datas = """SELECT date, who_is, etap_2 FROM voice_data WHERE date >= '2020-07-01' AND date <= '2020-08-31'"""
cursor.execute(datas)
connection.commit()
mobile_records = cursor.fetchall() 

for row in mobile_records:
    print("Дата:", row[0], )
    print("Результат первого этапа:", row[1],)
    print("Результат второго этапа:", row[2], "\n")

cursor.close()
connection.close()


connection = psycopg2.connect(dbname="x-lab_voice", user="postgres", password="faqser95", host="localhost", port='5432')
cursor = connection.cursor()

datas = """SELECT date, who_is, etap_2 FROM voice_data WHERE date >= '2020-08-29' AND date <= '2020-08-31'"""
cursor.execute(datas)
connection.commit()
mobile_records = cursor.fetchall() 

for row in mobile_records:
    print("Дата:", row[0], )
    print("Результат первого этапа:", row[1],)
    print("Результат второго этапа:", row[2], "\n")


datas_1 = """SELECT who_is, duration FROM voice_data WHERE who_is = 'Human'"""
cursor.execute(datas_1)
connection.commit()
records_1 = cursor.fetchall() 

datas_2 = """SELECT COUNT(*) FROM voice_data WHERE who_is = 'Human'"""
cursor.execute(datas_2)
connection.commit()
records_2 = cursor.fetchall() 

datas_3 = """SELECT description_2, hostname, ip_address FROM fk_server"""
cursor.execute(datas_3)
connection.commit()
records_3 = cursor.fetchall()

datas_4 = """SELECT name_1, description_1 FROM fk_project"""
cursor.execute(datas_4)
connection.commit()
records_4 = cursor.fetchall() 

for row_1 in records_1:
    for row_2 in records_2:
        for row_3 in records_3:
            for row_4 in records_4:
                print("Реузльтат первого этапа:", row_1[0])
                print("Длительность аудио:", row_1[1],)
                print("Количество записей за указанную дату:", row_2[0])
                print("Описание 'Cервера':", row_3[0])
                print("Имя хоста:", row_3[1])
                print("ip-адрес:", row_3[2])
                print("Имя 'Проекта':", row_4[0])
                print("Описание:", row_4[1],"\n")
