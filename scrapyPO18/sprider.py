# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def login():
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://members.po18.tw',
            'Referer': 'https://members.po18.tw/apps/login.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/78.0.3904.108 Safari/537.36'
        }
        account = 'YOUR ACCOUNT'
        pwd = 'YOUR PASSWORD'
        data = {
            'account': account,
            'pwd': pwd,
            'remember_me': '1',
            'comefrom_id': '2',
            'owner': 'COC',
            'client_ip': 'YOUR IP',
            'url': 'https://www.po18.tw/'
        }
        login_url = 'https://members.po18.tw/apps/login.php'
        login_html = session.post(login_url, data=data, headers=headers, timeout=10)
        if login_html.url == 'https://members.po18.tw/apps/login.php':
            print('Incorrect username or password, please check and re-edit.')
        elif login_html.url == 'https://www.po18.tw' or 'https://www.po18.tw/panel':
            print('Welcome, ' + account + '. The spider is working...')
            return True
        else:
            print(login_html)
            print('Unknown error.')
        return False
    except requests.exceptions.ConnectionError:
            print('ConnectionError, re-login...')
            login()
    except requests.exceptions.ReadTimeout or RuntimeError:
            print('Timeout, re-login...')
            login()


def getContent(page):
    global content_url
    if page > 1:
        content_url = content_url + '?page=' + str(page)
    response = session.get(content_url)
    print('page %d %s processing...' % (page, content_url))
    soup = BeautifulSoup(response.text, 'lxml')
    chapter_list = soup.find_all(name='a', attrs={'class': 'btn_L_blue'})

    global start
    for i in range(start, len(chapter_list)):
        chapter_url = 'https://www.po18.tw' + chapter_list[i].get('href')
        print('%d %s processing...' % (i, chapter_url))
        getChapter(chapter_url, 10)

    global chapter_sum
    if (chapter_sum - page*100) > 1:
        page += 1
        getContent(page)


def getChapter(chapter_url, time):
    try:
        text_url = chapter_url.replace("articles", "articlescontent")
        headers = {
            'Referer': chapter_url
        }
        response = session.get(text_url, headers=headers, timeout=10)
        chapter = response.text.replace("&nbsp;&nbsp;", '')
        soup = BeautifulSoup(chapter, 'lxml')
        chapter_title = soup.find('h1').get_text()
        if len(soup.find_all('p')) < 10:
            time = time - 1
            print('Unknown error, reloading... %d' % (11 - time))
            session.getChapter(chapter_url, time)
        if time == 1:
            print('Failed, pass.')
            pass
        else:
            print('%s processing...' % (chapter_title))
            txt.write(chapter_title + '\n')
            text = soup.find_all(name='p')
            for row in text:
                txt.write(row.get_text())
            print('%s done.' % chapter_title)
    except requests.exceptions.ConnectionError:
        print('ConnectionError, reloading...')
        session.getChapter(chapter_url, time)
    except requests.exceptions.ReadTimeout or RuntimeError:
        print('ReadTimeout or RuntimeError, reloading...')
        session.getChapter(chapter_url, time)


book_number = 'YOUR TARGET BOOK'
content_url = 'https://www.po18.tw/books/' + book_number + '/articles'
chapter_sum = 000
start = 0
session = requests.session()
if login():
    txt = open('YOUR PATH' + book_number + '.txt', 'a')
    getContent(1)
    txt.close()
