import requests
from lxml import etree

url_root = "http://www.biquge.info/wanjiexiaoshuo/"
for i in range(1, 456):
    url = url_root + str(i)
    r = requests.get(url)
    html = etree.HTML(r.text)
    links = html.xpath('//*[@id="main"]/div[1]/ul/li/span[2]/a/@href')
    for link in links:
        with open('novel_links.txt', 'a') as f:
            f.write(link + "\n")
