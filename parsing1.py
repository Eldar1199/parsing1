import requests
from bs4 import BeautifulSoup
import csv
def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'],
                         data['img'],
                         data['desc'],
                         data['price']])


def get_html(url):
    response = requests.get(url)
    return  response.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    page_list = soup.find('div',  class_ = 'pager-wrap').find_all('li')
    last_page = page_list[-1].text
    return int(last_page)


def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    product_list = soup.find('div', class_ = 'list-view').find_all('div', class_ = 'item')
    # print(product_list)
    for product in product_list:
        title = product.find('div', class_ = 'listbox_title').find('strong').text
        # print(title)
        img = 'https://www.kivano.kg/' + product.find('img').attrs.get('src')
        # print(img)
        desc = product.find('div', class_ = "product_text").text.replace(title, '').strip()
        # print(desc)
        price = product.find('div', class_ = 'listbox_price').text.strip()
        # print(price)
        product_dict = {'title': title,
                        'img': img,
                        'desc': desc,
                        'price': price}
        write_to_csv(product_dict)


def main():
        notebook_url = "https://www.kivano.kg/noutbuki"
        html = get_html(notebook_url)
        get_data(html)
        number = get_total_pages(html)
        for i in range(2, number+1):
             url_with_page = notebook_url + '?page=' + str(i)
             html = get_html(url_with_page)
             get_data(html)


with open('data.csv', 'w') as file:
    write_ = csv.writer(file)
    write_.writerow(['title     ', 'img       ', 'desc      ', 'price      '])

main()