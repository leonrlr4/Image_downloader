# import requests
# from bs4 import BeautifulSoup as bs

# def download_pic(url, path):
#     pic = requests.get(url)
#     f = open(path, 'wb')
#     f.write(pic.content)
#     f.close()
# url = 'https://cdn.pixabay.com/photo/2015/06/08/15/02/pug-801826__340.jpg'
# pic_path = '/Users/tobias/Desktop/未命名檔案夾/'+ url[url.rfind('/'):]

# def get_photos(photo_name, download_num):
#     page = 1
#     photo_list = []

#     while True:
#         url = 'https://pixabay.com/zh/photos/' + photo_name + '/?pagi=' + str(page)
#         html = requests.get(url)
#         html.encoding = 'utf-8'
#         bsObj = bs(html.text, 'lxml')
#         photo_item = bs.find_all('div', {'class': 'item'})

#         if len(photo_item) == 0:
#             return None
#         for i in range len(photo_item):

# url = 'https://cdn.pixabay.com/photo/2015/06/08/15/02/pug-801826__340.jpg'
# pic_path = '/Users/tobias/Desktop/未命名檔案夾/'+ url[url.rfind('/'):]


import requests
from bs4 import BeautifulSoup as bs
import lxml
from lxml import etree
import os
import threading

def download_pic(url, path):
    pic = requests.get(url)
    f = open(path, 'wb')
    f.write(pic.content)
    f.close()



def get_photolist(photo_name, download_num):
    page = 1
    photo_list = []

    while True:
        url  = 'https://pixabay.com/zh/photos/' + photo_name + '/?pagi=' + str(page)
        html =  requests.get(url)
        bsObj = bs(html.text, 'lxml')
        scope = bsObj.find_all('div', {'class': 'item'})

        for i in scope:
            lazy = i.find('img')
            if lazy['src'] != '/static/img/blank.gif':
                photo_list.append(lazy['src'])
            else:
                photo_list.append(lazy['data-lazy'])

            if len(photo_list) >= download_num:
                return photo_list
        page+=1



def create_folder(photo_name):
    folder_name = input('請輸入資料解名稱： ')
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f'資料夾不存在， 已建立{folder_name}資料夾')
    else:
        print(f'找到資料夾: {folder_name}')

    if not os.path.exists(folder_name + os.sep + photo_name):
        os.mkdir(folder_name + os.sep + photo_name)
        print(f'建立資料夾： {photo_name}')
    else:
        print(f'"{photo_name} "資料夾已存在')
    return folder_name


def get_photobythread(folder_name, photo_name, photo_list):
    download_num = len(photo_list)
    q = int(download_num / 100)
    r = download_num % 100
    for i in range(q):
        threads = []
        for j,o in zip(range(100), photo_list):
            threads.append(threading.Thread(target = download_pic, args = (photo_list[i*100+j], folder_name + os.sep + photo_name + os.sep + o[o.rfind('/'):])))
            threads[j].start()
        for j in threads:
            j.join()
        print(int((i+1)*100/download_num*100), '%')
    threads = []
    for i, p in zip(range(r), photo_list):
        threads.append(threading.Thread(target = download_pic, args = (photo_list[q*100+i], folder_name + os.sep + photo_name + os.sep + p[p.rfind('/'):])))
        threads[i].start()
    for i in threads:
        i.join()
    print('100%')
