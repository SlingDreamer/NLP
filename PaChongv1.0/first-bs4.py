import requests
import json
import re
import time
import threading
import bs4


def get_item(soup):
    link = soup.find('ul', class_="c1text3")
    link1 = link.find_all('li')
    j = 0
    item = {}
    for i in link1:
        if j==4:
            # print(str(i.text[0:5]).strip().replace('\n','') + ':' + str(i.text[5:]).strip().replace('\n',''))
            item[str(i.text[0:5]).strip().replace('\n','')] = str(i.text[5:]).strip().replace('\n','')
            j = j+1
            continue
        # print(str(i.text[0:4]).strip().replace('\n','') + ':' + str(i.text[4:]).strip().replace('\n',''))
        item[str(i.text[0:4]).strip().replace('\n','') ] =  str(i.text[4:]).strip().replace('\n','')
        j = j+1
    return item

def get_price(soup):
    link = soup.find('p', class_="c1text2")

    link1 = link.find_all('span')

    j = 0
    price = {}
    for i in link1:
        if j == 0:
            # print(str(i.text[0:4]).strip().replace('\n','') + ':' + str(i.text[6:-4]).strip().replace('\n',''))
            price[str(i.text[0:4]).strip().replace('\n','')] = str(i.text[6:-4]).strip().replace('\n','')
            j = j + 1
            continue
        # print(str(i.text[0:4]).strip().replace('\n','') + ':' + str(i.text[6:-2]).strip().replace('\n',''))
        price[str(i.text[0:4]).strip().replace('\n','')] = str(i.text[6:-2]).strip().replace('\n','')
    return price

def get_maofa(soup):
    # url = 'http://dog.goumin.com' + detail
    # r = requests.get(url=url)
    # str1 = r.text
    # soup = bs4.BeautifulSoup(str1, "html.parser")
    link = soup.find_all('a',class_ = 'typea')

    j = 0
    link1 = soup.find_all('dl', class_="typedl type1")

    maofa = {}
    for i in link:
        # print(str(i.text).strip().replace('\n','')+' : '+ str(link1[j].text).strip())
        maofa[str(i.text).strip().replace('\n','')] = str(link1[j].text).strip()
        j = j+1
    return maofa

def get_xinge(soup):
    # url = 'http://dog.goumin.com' + detail
    # r = requests.get(url=url)
    # str1 = r.text
    # soup = bs4.BeautifulSoup(str1, "html.parser")
    link = soup.find('ul',class_ = 'con2list')
    link1 = link.find_all('li')


    link2 = soup.find_all('div', class_="neirongs")

    xingge = {}
    for i in link2:
        i = str(i.text).strip()
        i = i.split('\n\n')
        if len(i)>1:
            str2 = ''
            for k in i[1:]:
                str2 = str2 + k.strip().replace('\n','') + ';'
            # print(i[0].strip().replace('\n','')+' : '+str2)
            xingge[i[0].strip().replace('\n','')] = str2
            continue
        # print(i[0]+' :  '.strip().replace('\n',''))
        xingge[i[0]] = ''
    return xingge

def get_dog(detail):
    url = 'http://dog.goumin.com'+detail
    r = requests.get(url=url)
    str1 = r.text
    soup = bs4.BeautifulSoup(str1, "html.parser")
    return soup


# s = get_dog('/pet/133.html')
# get_price(s)
# get_item(s)
# get_maofa(s)
# get_xinge(s)



def do_all(s):
    prince = get_price(s)
    item = get_item(s)
    maofa = get_maofa(s)
    xinge = get_xinge(s)

    ani_class = {}

    for key in prince:
        ani_class[str(key).replace(u'\xa0', u' ')] = str(prince[key]).replace(u'\xa0', u' ').replace(u'\u301c', u' ').replace(u'\u2027', u'.')

    for key in item:
        ani_class[str(key).replace(u'\xa0', u' ')] = str(item[key]).replace(u'\xa0', u' ').replace(u'\u301c', u' ').replace(u'\u2027', u'.')

    for key in maofa:
        ani_class[str(key).replace(u'\xa0', u' ')] = str(maofa[key]).replace(u'\xa0', u' ').replace(u'\u301c', u' ').replace(u'\u2027', u'.')

    for key in xinge:
        ani_class[str(key).replace(u'\xa0', u' ')] = str(xinge[key]).replace(u'\xa0', u' ').replace(u'\u301c', u' ').replace(u'\u2027', u'.')

    # for key in ani_class:
    #     print(key+ ':' + ani_class[key])

    return ani_class

def store(data):
    with open('data1.json', 'a', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data,ensure_ascii=False))
        json_file.write('\n')

def get_g_son():
    t_url = 'http://dog.goumin.com/'
    r = requests.get(url=t_url)
    str1 = r.text

    soup = bs4.BeautifulSoup(str1, "html.parser")
    link = soup.find_all('a', href=re.compile('^/pet/'))

    all_animal ={}

    j = 0
    k = 0

    for i in link:
        k = k+1
        try:
            if str(i.text) == '中牧':
                print(i.text)
                s = get_dog(str(i).split('\"')[1])
                all_animal[str(i.text)] = do_all( s)
                break

            print(i.text)
            s = get_dog(str(i).split('\"')[1])
            all_animal[str(i.text)] = do_all(s)
            j = j+1
            # if j>10:
            #     break
        except BaseException:
            continue

    print(j,k)
    for single in all_animal:
        s_ani = {}
        s_ani[single] = all_animal[single]
        store(s_ani)



get_g_son()