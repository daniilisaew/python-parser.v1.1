import requests
from bs4 import BeautifulSoup
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
HOST = 'https://besplatka.ua/'


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', id='pagination').find('ul', class_='pagination').findAll('li')[-2].text
    print("Total pages:",page)
    return int(page)



def save(data):
    with open('ads.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            [data['title'],
             data['url'],
             data['price'],
             data['quality'],
             data['region'], ])





def get_content(html):

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='msg-one')
    for item in items:

            try:
                title = item.find('div', class_='fl-100').get_text(strip=True)
            except:
                title = 'НЕТ ДАННЫХ'
            try:
                url = HOST + item.find('div', class_='msg-inner').find('a', class_='w-image').get('href').strip()
            except:
                url = 'НЕТ ДАННЫХ'
            try:
                price = item.find('p', class_='m-price').find('span').get_text(strip=True)
            except:
                price = 'НЕТ ДАННЫХ'
            try:
                quality = item.find('div', class_='w-body').find('div', class_='properties-list').get_text(strip=True)
            except:
                quality = 'НЕТ ДАННЫХ'
            try:
                region = item.find('li', class_='m-region').find('a').get_text(strip=True)
            except:
                region = 'НЕТ ДАННЫХ'

            items = {
                'title': title,
                'url': url,
                'price': price,
                'quality': quality,
                'region': region,
                }

            save(items)


def main():
    url ='https://besplatka.ua/electronika-i-bitovaya-tehnika'
    base_url = 'electronika-i-bitovaya-tehnika/'
    page = 'page/'
    pages = get_pages(get_html(url))

    pg = input("Enter a number of page what would you like to parse or write all if you want parse all pages: ")

    if pg == 'all':
        for i in range(0, pages):
            print(f'Parsing {i} page')
            url_f = HOST + base_url + page + str(i)

            html = get_html(url_f)
            get_content(html)
    elif pg:
        for i in range(0, int(pg)):
            print(f'Parsing {i} page')
            url_f = HOST + base_url + page + str(i)

            html = get_html(url_f)
            get_content(html)
    else:
        print("Something went wrong(((")



if __name__ == '__main__':
    main()











