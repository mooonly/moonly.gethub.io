# -*- coding:utf-8  -*-
import re
import sys
import requests
import time
import queue
import argparse 
from config.config import *
import importlib
from lib.OutPut import Output
from concurrent.futures import ThreadPoolExecutor #线程池，进程池


#解决ssl告警
requests.packages.urllib3.disable_warnings()


class Url_Spider:
    def __init__(self,domain,subdomain,todo_url_list,layers,config):
        self.target = domain
        self.subdomain = subdomain
        self.todo_url_list = []
        self.max_layers = layers
        self.config = config
        self.session = requests.session()
        self.output = Output()
        self.queue = queue.Queue()
        self.rules = config['rules']
        self.rules['domain'] = r'(https?|http):\/\/[\d\w\-\.\#]*' + self.subdomain + '/'
        self.headers = config['headers']
        self.spider_ua_types = config['Spider_UA'].keys()
        self.succurl_lists = set()
        self.result_data = {
            'img': 0,
            'domain':0,
            'crossdomain':0,
            'file':0,
            'static':0,
        }
        self.url_check(todo_url_list)
       
        



    def url_check(self,result_lists):
        for url_list in result_lists:
            url = url_list[0]
            source_url = url_list[1]
            for rule_type,rule in self.rules.items():
                if re.match(rule,url,re.IGNORECASE) != None :
                    self.result_data[rule_type] += 1
                    self.output.write_csv(url,source_url,rule_type) #写入文件
                    if rule_type in ['static','domain']  and url not in self.succurl_lists: 
                        self.todo_url_list.append([url,source_url])
                        self.succurl_lists.add(url)
                        #print(f'\t[{rule_type}] [put] {url} [from] {source_url}')
                    break
    
    def create_queue(self):
        self.queue.queue.clear() 
        for url_list in self.todo_url_list:
            url = url_list[0]
            source_url = url_list[1]
            for ua_type in self.spider_ua_types:
                self.queue.put([url,source_url,ua_type,1])

    def queueurl_check(self,result_lists):
        for url_list in result_lists:
            url = url_list[0]
            source_url = url_list[1]
            ua_type = url_list[2]
            layers = url_list[3]
            for rule_type,rule in self.rules.items():
                if re.match(rule,url,re.IGNORECASE) != None :
                    self.result_data[rule_type] += 1
                    self.output.write_csv(url,source_url,rule_type) #写入文件
                    if rule_type in ['static','domain']  and url not in self.succurl_lists: 
                        self.queue.put([url,source_url,ua_type,layers])
                        self.succurl_lists.add(url)
                        #print(f'\t[{rule_type}] [put] {url} [from] {source_url}')
                    break

    def end_print(self):
        decode = {
            'img': '图片',
            'domain':'url',
            'crossdomain':'外链',
            'file':'文件',
            'static':'前端文件',
        }
        for url_type,num in self.result_data.items():
            print(f'\t发现{decode[url_type]}{num}个')

    def run(self):
        plug = self.config['scan_plug_in_unit']
        print(f'动态加载插件库,加载插件数:{len(plug)}')
        #动态加载插件获取url
        for scan_plug in self.config['scan_plug_in_unit']:
            plug_in_unit = getattr(importlib.import_module(f"lib.{scan_plug}"),'BaiduSpider')
            spider = plug_in_unit(self.target,self.output,self.config)
            result_lists = spider.run()
            print(f'[scan_plug] {scan_plug} [end] get {len(result_lists)}')
            self.url_check(result_lists)
        #主体爬虫程序
        print('插件库执行终了，执行爬取')
        print(f'目标:{self.target} 待爬取链接数:{len(self.todo_url_list)} UA数:{len(self.spider_ua_types)}' )
        from lib.HtmlSpider import HtmlSpider
        self.create_queue()
        number = 0 
        htmlSpider = HtmlSpider(self.output,self.config,self.max_layers)
        while not self.queue.empty():
            number += 1 
            target_data = self.queue.get()
            max_number = self.queue.qsize()
            url = target_data[0]   #目标url
            source_url = target_data[1]  #ua类 
            ua_type = target_data[2]    #来源url
            layers = target_data[3]  #层数
            result_lists = htmlSpider.run(url,ua_type,source_url,layers)
            self.queueurl_check(result_lists)
            print(f'succ:{number} todo:{max_number} layers:{layers} geturl:{len(result_lists)} [{url}]                                                                   ',end='\r')
        print('\n[终了]')
        self.end_print()
        

def parse_args():
    """
    :return:进行参数的解析
    """
    description = "缺少指定参数"                   # 步骤二
    parser = argparse.ArgumentParser(description=description)        # 这些参数都有默认值，当调用parser.print_help()或者运行程序时由于参数不正确(此时python解释器其实也是调用了pring_help()方法)时，
    parser.add_argument('domain',help='指定目标域名') 
    parser.add_argument('--layers','-l',help='指定爬取最大层数',type=int,default=5) 
    parser.add_argument('--url','-u',help='指定爬取的URL，需同目标域名')     
    parser.add_argument('--urlList','-uL',help='指定爬取的URL列表，需同目标域名')  
    parser.add_argument('--cookie','-c',help='指定cookie')
    parser.add_argument('--headers','-H',help='指定特殊headers头参数')          
    args = parser.parse_args()                                       # 步骤四          
    return args

def domain_check(domain):
    tmp_list = domain.split('.')
    if len(tmp_list) == 2 :
        maindomain = f'www.{tmp_list[0]}.{tmp_list[1]}'
        subdomain = str(tmp_list[0] + '.' +tmp_list[1])
    elif len(tmp_list) == 3:
        maindomain = domain
        subdomain = str(tmp_list[1] + '.' +tmp_list[2])
    elif len(tmp_list) == 4 and re.match(r'[a-zA-Z]+',domain) == None:
       maindomain = domain
       subdomain = domain
    else:
        print(f'{domain}格式错误')
        exit()
    subdomain = subdomain.split(':')[0]
    return {'maindomain':maindomain,'subdomain':subdomain}


if __name__ == "__main__":
    todo_url_list = []
    args = parse_args()
    target_data = domain_check(args.domain)
    if args.urlList  != None:
       for url in set(args.urlList.split(',')):
        todo_url_list.append([url,'init'])
    if args.url != None:
        todo_url_list.append([args.url,'init'])
    if args.layers != None:
        layers = args.layers
    else:
        layers = config['layers']
    if args.cookie != None:
        config['headers']['cookie'] = args.cookie
    if args.headers != None:
        for header in set(args.headers.split(',')):
            tmp_list = header.split(':')
            config['headers'][tmp_list[0]] = tmp_list[1]
    test = Url_Spider(target_data['maindomain'],target_data['subdomain'],todo_url_list,layers,config)
    test.run()


