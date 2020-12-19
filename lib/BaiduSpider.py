import requests
import re
from bs4 import BeautifulSoup
import queue

class BaiduSpider:
    def __init__(self,domain,output,config):
        self.queue = queue.Queue()
        self.result_lists = []
        self.output = output
        self.target = domain
        self.pattern = re.compile(r'href="https?://www.baidu.com/link\?url=[-\d_\w]+') 
        self.session = requests.session()
        self.urls = set()
        self.key_words = config['baidu_words']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }


    def get_url(self,url):
        r = self.session.get(url = url,timeout=5,headers = self.headers,verify=False)
        urls = self.pattern.findall(r.text)
        for url in urls:
            url = url[6:]
            res = self.session.get(url = url,timeout=5,headers = self.headers,allow_redirects=False)
            if res.status_code == 302:
                self.result_lists.append([res.headers['Location'],'http://www.baidu.com'])
            elif res.status_code == 200:
                print(res.url)
                print('200 exit')  #可能会出现200的情况，需要额外处理
                exit()

    def create_queue(self,num):
        self.queue.queue.clear() 
        print(f'[BaiduSpider] 关键字个数{len(self.key_words)};单个关键字爬取条数{num}')
        for key_word in self.key_words:
            for i in range(0,num,10):
                self.queue.put("http://www.baidu.com/s?tn=monline_4_dg&ie=utf-8&wd=inurl%3A" + self.target + '%20' + key_word + '&pn=' + str(i) )
        

    def run(self):
        self.session.get(url='http://www.baidu.com',timeout=5,headers = self.headers)
        self.create_queue(30)
        number = 0 
        max_number = self.queue.qsize()
        while not self.queue.empty():
            number += 1
            print(f'[{self.target}] {number}/{max_number}',end='\r')
            url = self.queue.get()
            self.get_url(url)
        print('\nend')
        return self.result_lists
