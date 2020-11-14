import requests
import time
from lxml import etree
from requests.adapters import HTTPAdapter


class NovelDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
        with open('novel_links.txt', 'r') as f:
            self.links = f.readlines()

    def download(self):
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        # 爬取前30本小说
        for link in self.links[0:30]:
            print('flag')
            try:
                # 请求小说链接
                r = requests.get(link, headers=self.headers, timeout=10)
            except:
                print('网络错误(1)')
                while True:
                    try:
                        r = requests.get('http://www.baidu.com')
                        if r.status_code == 200:
                            r = requests.get(link, headers=self.headers, timeout=10)
                            break
                    except:pass
            time.sleep(1)
            # 页面解析
            html = etree.HTML(r.text.encode('ISO-8859-1').decode('utf-8', "ignore"))
            # 小说名
            title = html.xpath('//*[@id="info"]/h1/text()')[0]
            # 作者
            author = html.xpath('//*[@id="info"]/p[1]/text()')[0].replace('作    者:', '')
            # 类别
            category = html.xpath('//*[@id="info"]/p[2]/text()')[0].replace('类    别:', '')
            # 最后更新时间
            lastUpdate = html.xpath('//*[@id="info"]/p[3]/text()')[0].replace('最后更新  :', '')
            # 描述
            descriptions = html.xpath('//*[@id="intro"]/p[1]')[0].xpath('string(.)')
            # 封面地址
            picture = html.xpath('//*[@id="fmimg"]/img/@src')[0]
            # 章节地址
            chapter_links = html.xpath('//*[@id="list"]/dl/dd/a/@href')
            # 章节名
            chapter_names = html.xpath('//*[@id="list"]/dl/dd/a/text()')
            # print(title, author, category, lastUpdate, picture, chapter_links, chapter_name)
            p = requests.get(picture)
            with open('./' + title + '.jpg', 'wb') as f:
                f.write(p.content)
            with open('./' + title + '.txt', 'w') as f:
                f.write(title + '\n' + author + '\n' + category + '\n' + lastUpdate + '\n' +
                        descriptions + '\n')
            flag = 0
            for chapter_link in chapter_links:
                time.sleep(3)
                # print('------------' + '\n' + chapter_names[flag] + '\n')
                # flag += 1
                with open('./' + title + '.txt', 'a') as f:
                    f.write('------------' + '\n' + chapter_names[flag] + '\n')
                    flag += 1
                try:
                    c = requests.get(link.replace('\n', '') + chapter_link, headers=self.headers, timeout=10)
                    html = etree.HTML(c.text.encode('ISO-8859-1').decode('utf-8', "ignore"))
                    contents = html.xpath('//*[@id="content"]//text()')
                    for content in contents:
                        # print(content.replace('\xa0', ' ').replace('\u30fb', '.'))
                        with open('./' + title + '.txt', 'a') as f:
                            f.write(content.replace('\xa0', ' ').replace('\u30fb', '.') + '\n')
                except:
                    print('网络错误(2)')
                    while True:
                        try:
                            r = requests.get('http://www.baidu.com')
                            if r.status_code == 200:
                                c = requests.get(link.replace('\n', '') + chapter_link, headers=self.headers, timeout=10)
                                html = etree.HTML(c.text.encode('ISO-8859-1').decode('utf-8', "ignore"))
                                contents = html.xpath('//*[@id="content"]//text()')
                                for content in contents:
                                    # print(content.replace('\xa0', ' ').replace('\u30fb', '.'))
                                    with open('./' + title + '.txt', 'a') as f:
                                        f.write(content.replace('\xa0', ' ').replace('\u30fb', '.') + '\n')
                                break
                        except:pass


download = NovelDownloader()
download.download()
