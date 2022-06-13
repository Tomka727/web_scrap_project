from lxml import html
import config as cfg
import requests
import re
import csv

response = requests.get('https://provanmotors.be/NL/stock/jonge2dehands.aspx?p=1')

tree = html.fromstring(response.content)

if (cfg.pages_to_read == 0):
    last_page = int(tree.xpath("(//div[@class='pages']/*)[last()]/text()")[0])
else:
    last_page = cfg.pages_to_read

links = []
for i in range(1, last_page+1):
  response = requests.get(f'https://provanmotors.be/NL/stock/jonge2dehands.aspx?p={i}')
  tree = html.fromstring(response.content)
  links += (tree.xpath("//a[@class='card']/@href"))


def scrape_from_page(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    content = dict()
    content['title'] = tree.xpath("//h1[@class='mobile-pt']/text()")[0]
    #content['price'] = re.sub('[^0-9]', '', tree.xpath("//div[@class='card-panel active']//dd/text()")[0])
    content['price'] = re.sub('[^0-9]', '', tree.xpath("//div[@class='price']/text()")[0])
    content['images'] = tree.xpath("//div[@class='stock-thumbs']/a/@href")[0]

    return content


filename = "results.csv"
head = ['ID', 'Title', 'Price', 'Image']

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(head)

    for i in range(0, len(links)):

        car_info = scrape_from_page('https://provanmotors.be' + links[i])
        row = [i+1, car_info['title'], car_info['price'], 'https://provanmotors.be' + car_info['images']]
        csvwriter.writerow(row)
