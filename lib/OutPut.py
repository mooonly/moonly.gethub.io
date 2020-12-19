import re
import xlsxwriter
import hashlib
import time
import csv

class Output():
    def __init__(self):
        self.files = {}
        self.csvs = {}
        self.nums = {}
        self.url_type = {
            'img':'./output/img_url.csv',
            'static':'./output/static_url.csv',
            'error':'./output/error_url.csv',
            'crossdomain':'./output/crossdomain_url.csv',
            'file':'./output/file_url.csv',
            'domain':'./output/domain_url.csv'
            }
        self.bt = ['序号','url','类型']
        self.create_csv()

    def out_html(self,url,sou_url,html_text,ua_type,path):
        ticks = time.time()
        m_str = 'uyfiugoihlkjcjh' + str(ticks)
        m = hashlib.md5(m_str.encode(encoding='gb2312'))
        file_name = './output/'+ path + '/' + m.hexdigest() + '.html'
        html_file = open(file_name,"w",encoding='utf-8')
        html_file.write(f'url:{url}\n')
        html_file.write(f'ua_type:{ua_type}\n')
        html_file.write(f'sou_url:{sou_url}\n')
        html_file.write(f'time:{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }\n')
        html_file.write(html_text)
        html_file.close()

    def create_csv(self):
        for url_type,file_name in self.url_type.items():
            self.files[url_type] = open(file_name, "a+",encoding='utf-8-sig')
            self.csvs[url_type] = csv.writer(self.files[url_type])
            self.nums[url_type] = 1
            #self.csvs[url_type].writerow(['文件名','url','来源URL','检测结果']) 

    def write_csv(self,url,sou_url,url_type,error_code=None):
        tmp_list = [self.nums[url_type],url,sou_url,url_type,error_code]
        #print(tmp_list)
        self.csvs[url_type].writerow(tmp_list)
        self.nums[url_type] += 1

    def close(self):
        #for url_type in self.url_type.keys():
        #    self.xlsxs[url_type].close()
        for url_type in self.url_type.keys():
            self.files[url_type].close()

"""
output = Output()
data = [
    ['http://21ada.qwesa.1','img'],
    ['http://21ada.qwesa.2','img'],
    ['http://21ada.qwesa.3','img'],
    ['http://21ada.qwesa.1','static'],
    ['http://21ada.qwesa.4','img'],
    ['http://21ada.qwesa.5','img'],
    ['http://21ada.qwesa.2','static'],
    ['http://21ada.qwesa.6','img'],
    ['http://21ada.qwesa.7','img'],
    ['http://21ada.qwesa.3','static'],
    ['http://21ada.qwesa.8','img'],
    ['http://21ada.qwesa.9','img'],
    ['http://21ada.qwesa.10','img'],
    ['http://21ada.qwesa.4','static'],
    ['http://21ada.qwesa.11','img'],
    ['http://21ada.qwesa.12','img'],

]
for row in data:
    output.write_csv(row[0],row[1])
output.close()

#output.out_html('http://1123.123123.123123./1231','123')
"""