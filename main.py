# -*- coding: utf-8 -*-
import requests
import json
import sqlite3
import os

# Дополнительные функции
import datetime
from datetime import datetime
import wikipedia
import math as m
import numpy as np
import random
from bs4 import BeautifulSoup

# Для работы с ВК
import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

# Список функций
help = ['\n Функции бота:',
        '\n help: Вывод всех доступных команд',
        '\n wiki: Поиск нужной информации в википедии',
        '\n wiki_tr: Поиск нужной информации в википедии, с переводом на нужный язык, (wiki_tr ru intel)',
        '\n news: Последние новости',
        '\n news_old: Давние новости',
        '\n trans: Переводчик, (trans ru-en Привет)',
        '\n date: Текущая дата',
        '\n time: Текущее время',
        '\n joke: Шутка',
        '\n img: Смешная картика',
        '\n task: Решить задачу',
        '\n +: Сложение, x+y...+z',
        '\n -: Вычитание, x-y...-z',
        '\n *: Умножение, x*y...*z',
        '\n /: Деление, x/y',
        '\n ^: Степень, x^y',
        '\n log2: Логарифм по 2',
        '\n log10: Логарифм по 10',
        '\n sqrt: Квадратный корень\n',

        '\n Дополнительная информация:'
        '\n language: Вывод языков для работы с переводом, и их сокращения'
        ]

token = '***'
vk_session = vk_api.VkApi(token = token)
url_translate = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
key_translate = 'trnsl.1.1.20190227T075339Z.1b02a9ab6d4a47cc.f37d50831b51374ee600fd6aa0259419fd7ecd97'

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                message_text = str(event.text).lower()
                #Слушаем longpoll, если пришло сообщение то:
                if 'date' in message_text: # Местная дата
                    vk.messages.send( #Отправляем сообщение
                        user_id = event.user_id,
                        message = datetime.now().strftime("%Y.%m.%d  %H:%M"),
                        random_id = get_random_id()
        		    )
                elif 'trans' in message_text: # Переводчик
                    mas_trans = message_text.replace('trans', '')
                    lang =  mas_trans[:6]
                    text = mas_trans[7:]
                    result = requests.post(url_translate, data={'key': key_translate, 'text': text, 'lang': lang})
                    vk.messages.send(
                        random_id = get_random_id(),
                        message = json.loads(result.text)['text'][0],
                        user_id = event.user_id,
                    )
                elif 'time' in message_text: # Местное время
                    vk.messages.send(
                        user_id = event.user_id,
                        message = datetime.now().strftime("%H:%M:%S"),
                        random_id = get_random_id()
        		    )
                elif 'log2' in message_text: # log2
                    num =  float(message_text[5:])
                    vk.messages.send(
                        user_id = event.user_id,
                        message = m.log2(num),
                        random_id = get_random_id()
        		    )
                elif 'tens_d' in message_text: # Умножение тензора
                    input = str(message_text[6:])
                    for i in range(len(input)):
                        if str(input[i]) == '*':
                            sign = '*'
                            sign_id = i
                        if str(input[i]) == '-':
                            sign = '-'
                            sign_id = i
                        if str(input[i]) == '+':
                            sign = '+'
                            sign_id = i
                        if str(input[i]) == '/':
                            sign = '/'
                            sign_id = i
                        if str(input[i]) == '**':
                            sign = '**'
                            sign_id = i
                    y = input[sign_id]
                    x = float(input[sign_id+2:])
                    res = list()
                    st = list()
                    mas_tens = input.replace(',', ' ')
                    mas_tens = mas_tens.replace('[', '')
                    mas_tens = mas_tens.replace(']', '')
                    mas_tens = mas_tens + ' '
                    a = 0
                    for i in range(sign_id-1):
                        if str(mas_tens[i]) == ' ':
                            b = i
                            res.append(mas_tens[a:b])
                            a = b + 1
                    del res[0]
                    for i in res:
                        st.append(float(i))
                    np_arr = np.array(st)
                    if y == '*':
                        result = np_arr * x
                    elif y == '-':
                        result = np_arr - x
                    elif y == '+':
                        result = np_arr + x
                    elif y == '/':
                        result = np_arr / x
                    elif y == '**':
                        result = np_arr ** x
                    vk.messages.send(
                        user_id = event.user_id,
                        message = [result],
                        random_id = get_random_id()
        		    )
                elif 'log10' in message_text: # log10
                    num =  float(message_text[6:])
                    vk.messages.send(
                        user_id = event.user_id,
                        message =  m.log10(num),
                        random_id = get_random_id()
        		    )
                elif 'sqrt' in message_text: # Квадратный корень
                    num =  int(message_text[5:])
                    vk.messages.send(
                        user_id = event.user_id,
                        message =  m.sqrt(num),
                        random_id = get_random_id()
        		    )
                elif '^' in message_text: # Степень
                    mas_num = []; mas_plus = []; i = 0; j = 0; summ = 1
                    for symbol in message_text:
                        i += 1
                        if symbol == '^':
                            mas_plus.append(i)
                    for i in mas_plus:
                        mas_num.append(message_text[j:i-1])
                        j = i
                    mas_num.append(message_text[i:])
                    vk.messages.send(
                        user_id = event.user_id,
                        message = float(mas_num[0]) ** float(mas_num[1]),
                        random_id = get_random_id()
        		    )
                elif '+' in message_text: # Сложение
                    mas_num = []; mas_plus = []; i = 0; j = 0; summ = 0
                    for symbol in message_text:
                        i += 1
                        if symbol == '+':
                            mas_plus.append(i)
                    for i in mas_plus:
                        mas_num.append(message_text[j:i-1])
                        j = i
                    mas_num.append(message_text[i:])
                    for i in mas_num:
                        summ += float(i)
                    vk.messages.send(
                        user_id = event.user_id,
                        message = summ,
                        random_id = get_random_id()
        		    )
                elif '-' in message_text: # Вычитание
                    mas_num = []; mas_plus = []; i = 0; j = 0; summ = 0
                    for symbol in message_text:
                        i += 1
                        if symbol == '-':
                            mas_plus.append(i)
                    for i in mas_plus:
                        mas_num.append(message_text[j:i-1])
                        j = i
                    mas_num.append(message_text[i:])
                    summ = 2*float(mas_num[0])
                    for i in mas_num:
                        summ -= float(i)
                    vk.messages.send(
                        user_id = event.user_id,
                        message = summ,
                        random_id = get_random_id()
        		    )
                elif '*' in message_text: # Умножение
                    mas_num = []; mas_plus = []; i = 0; j = 0; summ = 1
                    for symbol in message_text:
                        i += 1
                        if symbol == '*':
                            mas_plus.append(i)
                    for i in mas_plus:
                        mas_num.append(message_text[j:i-1])
                        j = i
                    mas_num.append(message_text[i:])
                    for i in mas_num:
                        summ *= float(i)
                    vk.messages.send(
                        user_id = event.user_id,
                        message = summ,
                        random_id = get_random_id()
        		    )
                elif '/' in message_text: # Деление
                    mas_num = []; mas_plus = []; i = 0; j = 0; summ = 1
                    for symbol in message_text:
                        i += 1
                        if symbol == '/':
                            mas_plus.append(i)
                    for i in mas_plus:
                        mas_num.append(message_text[j:i-1])
                        j = i
                    mas_num.append(message_text[i:])
                    vk.messages.send(
                        user_id = event.user_id,
                        message = float(mas_num[0]) / float(mas_num[1]),
                        random_id = get_random_id()
        		    )
                elif 'wiki_tr' == message_text[:7]: # Поиск по вики c переводом
                    mas_trans = message_text.replace('wiki_tr', '')
                    lang =  'en-' + str(mas_trans[1:3])
                    text = mas_trans[4:]
                    try:
                        result = requests.post(url_translate, data={'key': key_translate, 'text': wikipedia.summary(text, sentences=2), 'lang': lang})
                        vk.messages.send(
                            user_id = event.user_id,
                            message =  json.loads(result.text)['text'][0],
                            random_id = get_random_id()
            		    )
                    except Exception as err:
                        vk.messages.send(
                            user_id = event.user_id,
                            message = str(err),
                            random_id = get_random_id()
            		    )
                elif 'wiki' in message_text: # Поиск по вики
                    search =  message_text [5:]
                    try:
                        vk.messages.send(
                            user_id = event.user_id,
                            message =  wikipedia.summary(search, sentences=2),
                            random_id = get_random_id()
            		    )
                    except Exception as err:
                        vk.messages.send(
                            user_id = event.user_id,
                            message = str(err),
                            random_id = get_random_id()
            		    )
                elif 'joke' in message_text: # Вывод шутки
                    conn = sqlite3.connect("mydatabase.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT text FROM joke")
                    rand = random.randint(1, len(cursor.fetchall())-1)
                    cursor.execute("SELECT text FROM joke WHERE id =" + str(rand))
                    vk.messages.send(
                        user_id = event.user_id,
                        message =  str(cursor.fetchall())[3:-4:1],
                        random_id = get_random_id()
        		    )
                elif 'task' in message_text: # Вывод задачи
                    conn = sqlite3.connect("mydatabase.db")
                    cursor = conn.cursor()
                    answer = list()
                    cursor.execute("SELECT * FROM task")
                    rand = random.randint(1, len(cursor.fetchall())-1)
                    cursor.execute("SELECT title, text, complexity FROM task WHERE id =" + str(rand))
                    answer.append('\nНазвание: ' + str(cursor.fetchall()[0][0]))
                    cursor.execute("SELECT title, text, complexity FROM task WHERE id =" + str(rand))
                    answer.append('\nЗадача: ' + str(cursor.fetchall()[0][1]))
                    cursor.execute("SELECT title, text, complexity FROM task WHERE id =" + str(rand))
                    answer.append('\nСложность: ' + str(cursor.fetchall()[0][2]))
                    vk.messages.send(
                        user_id = event.user_id,
                        message = answer,
                        random_id = get_random_id()
        		    )
                elif 'help' in message_text: # Хелпер
                    vk.messages.send(
                        user_id = event.user_id,
                        message =  help,
                        random_id = get_random_id()
        		    )
                elif 'img' in message_text: # Вывод смешной картинки
                    upload = VkUpload(vk)
                    response = upload.photo_messages('img/' + str(random.randint(1,10)) + '.jpg')[0]
                    owner_id = response['owner_id']
                    photo_id = response['id']
                    access_key = response['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    vk.messages.send(
                        random_id = get_random_id(),
                        user_id = event.user_id,
                        attachment = attachment
                    )
                elif 'news_old' in message_text: # Вывод смешной картинки
                    page = requests.get('http://mathemlib.ru/news/')
                    page.encoding = 'cp1251'
                    soup = BeautifulSoup(page.text, 'html.parser')

                    result = str()
                    result += soup.select('div')[8].select('tr')[4].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[5].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[6].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[7].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[8].get_text()
                    vk.messages.send(
                        random_id = get_random_id(),
                        message = result,
                        user_id = event.user_id,
                    )
                elif 'news' in message_text: # Вывод смешной картинки
                    page = requests.get('http://mathemlib.ru/news/')
                    page.encoding = 'cp1251'
                    soup = BeautifulSoup(page.text, 'html.parser')

                    result = str()
                    result += soup.select('div')[8].select('tr')[0].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[1].get_text() + '\n'
                    result += soup.select('div')[8].select('tr')[2].get_text()
                    vk.messages.send(
                        random_id = get_random_id(),
                        message = result,
                        user_id = event.user_id,
                    )
                elif 'language' == message_text: # Остановка
                    vk.messages.send(
                        user_id = event.user_id,
                        message = ['''
                        азербайджанский	az
                        малаялам	ml
                        албанский	sq
                        мальтийский	mt
                        амхарский	am
                        македонский	mk
                        английский	en
                        маори	    mi
                        арабский	ar
                        маратхи	    mr
                        армянский	hy
                        марийский	mhr
                        африкаанс	af
                        монгольский	mn
                        баскский	eu
                        немецкий	de
                        башкирский	ba
                        непальский	ne
                        белорусский	be
                        норвежский	no
                        бенгальский	bn
                        панджаби	pa
                        бирманский	my
                        папьяменто	pap
                        болгарский	bg
                        персидский	fa
                        боснийский	bs
                        польский	pl
                        валлийский	cy
                        португальский	pt
                        венгерский	hu
                        румынский	ro
                        вьетнамский	vi
                        русский	    ru
                        гаитянский (креольский)	ht
                        себуанский	ceb
                        галисийский	gl
                        сербский	sr
                        голландский	nl
                        сингальский	si
                        горномарийский	mrj
                        словацкий	sk
                        греческий	el
                        словенский	sl
                        грузинский	ka
                        суахили	    sw
                        гуджарати	gu
                        сунданский	su
                        датский	    da
                        таджикский	tg
                        иврит	    he
                        тайский	    th
                        идиш	    yi
                        тагальский	tl
                        индонезийский	id
                        тамильский	ta
                        ирландский	ga
                        татарский	tt
                        итальянский	it
                        телугу	    te
                        исландский	is
                        турецкий	tr
                        испанский	es
                        удмуртский	udm
                        казахский	kk
                        узбекский	uz
                        каннада	    kn
                        украинский	uk
                        каталанский	ca
                        урду	    ur
                        киргизский	ky
                        финский	    fi
                        китайский	zh
                        французский	fr
                        корейский	ko
                        хинди	    hi
                        коса	    xh
                        хорватский	hr
                        кхмерский	km
                        чешский	    cs
                        лаосский	lo
                        шведский	sv
                        латынь	    la
                    	шотландский	gd
                        латышский	lv
                        эстонский	et
                        литовский	lt
                        эсперанто	eo
                        люксембургский	lb
                        яванский	jv
                        малагасийский	mg
                        японский	ja
                        малайский	ms'''],
                        random_id = get_random_id()
                    )
                elif 'stop' in message_text: # Остановка
                    1/0
                else: # Есои команды нет
                    vk.messages.send(
                        user_id = event.user_id,
                        message = 'Напишите, пожалуйста, help',
                        random_id = get_random_id()
                    )
    except:
        vk.messages.send(
            user_id = event.user_id,
            message = 'Произошла непредвиденная ошибка, отправьте ее, пожалуйста, разработчику.',
            random_id = get_random_id()
        )
