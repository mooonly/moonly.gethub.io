import re 
import requests
import queue
from urllib.parse import urlparse

class HtmlSpider():
    def __init__(self,output,config,max_layers):
        self.output = output
        self.config = config
        self.max_layers = max_layers
        self.queue = queue.Queue()
        self.pattern = {
            1:re.compile(r'=[\"\'\(]?[\w\:\/\.\-\_]+[\"\'\)]?'),
            2:re.compile(r'\([\w\:\/\.\-\_]+\)'),
            3:re.compile(r'http[s]?:\/\/[\d\w\-\.\?\/\\\+\&\%\$\#\_\=]+')
        }
        self.html_text = None
        self.spider_ua = self.config['Spider_UA']
        self.supplement_rules = {
                'un_supplement': r'^https?:\/\/',   #不需要补全
                'url_supplement': r'^\.+\/',  #eg: ../sda ./da
                'protocol_supplement': r'^\/\/',    #eg://www.123.com
                'host_supplement': r'^\/',     #eg:/12/as/1.html
                'url_supplement':r'^[\w\-\_\d]+\/',     #eg: asdasd/1.html
                   }
        

    def get_html(self,url,headers):
        try:
            res = requests.get(url = url,timeout=10,headers=headers,allow_redirects=True,verify=False)
            if res.status_code == requests.codes.ok:
                res.encoding = res.apparent_encoding
                html_text = res.text 
                url = res.url
                url_parse = urlparse(url)
                supplement_list = {
                    'un_supplement': '',
                    'url_supplement': url[0:url.rfind('/')] + '/',
                    'host_supplement': url_parse.scheme + '://' + url_parse.netloc ,
                    'protocol_supplement': url_parse.scheme + ':'  ,
                    'url_supplement':url[0:url.rfind('/')] + '/',
                }
            else:
                html_text = None
                supplement_list = {}
        except Exception as e :
            html_text = None
            supplement_list = {}
            self.output.write_csv(url,headers["Referer"],'error',e) #写入文件
        return [html_text,supplement_list]


    def find_url(self,html_text,supplement_list):
        urls = set()
        if html_text != None:
            for rule_num in self.pattern.keys(): 
                for text in self.pattern[rule_num].findall(html_text):
                    url = text.strip('=').strip('"').strip("\'").strip(")").strip("(")
                    if re.search('[\.\/]',url) != None and url not in ['text/html','text/javascript','css.css','text/css'] :
                        tmp_url = self.supplement_url(url,supplement_list)
                        urls.add(tmp_url)
        else:
            urls = set()
        return urls
    
    def supplement_url(self,url,supplement_list):
        for rule_type,rule in self.supplement_rules.items():
            if re.search(rule,url) != None :
                return supplement_list[rule_type] + url
        return url

    def run(self,url,ua_type,sou_url,layers):
        result_lists = []
        if layers <= self.max_layers:
            headers = self.config['headers'].copy()
            headers["Referer"] = sou_url
            headers["User-Agent"] = self.spider_ua[ua_type]
            res_data = self.get_html(url,headers)
            html_text = res_data[0]
            supplement_list = res_data[1]
            if html_text != None:
                self.output.out_html(url,'baidu',html_text,ua_type,'html')
                urls = self.find_url(html_text,supplement_list)
                for new_url in urls :
                    result_lists.append([new_url,url,ua_type,layers+1])
        return result_lists
