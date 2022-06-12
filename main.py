from lxml import html
import requests
import re

response = requests.get('https://provanmotors.be/NL/stock/jonge2dehands.aspx?p=1')

tree = html.fromstring(response.content)

last_page = int(tree.xpath("(//div[@class='pages']/*)[last()]/text()")[0])

links = []
for i in range(1, last_page+1):
  response = requests.get(f'https://provanmotors.be/NL/stock/jonge2dehands.aspx?p={i}')
  tree = html.fromstring(response.content)
  links += (tree.xpath("//a[@class='card']/@href"))
#print(len(links))


def scrape_from_page(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)

    content = dict()
    content['price'] = int(re.sub('[^0-9]', '', tree.xpath("//div[@class='price']/text()")[0]))
    content['title'] = 'blabla'
    content['images'] = []

    return content


#print(scrape_from_page('https://provanmotors.be//NL/detail/Hyundai/iX35/9561.aspx?p=16&seg=17838'))