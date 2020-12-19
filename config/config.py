
config = {
       'rules':{
                'img': r'.*\.(jpg|png|gif|swf|jpg.1|ico|ashx|jpeg|bmp|svg)$',
                'static': r'.*\.(js|css)$',
                'file':r'.*\.(pdf|xlsx|xls|docx|zip|rar|7z|mp4|doc|apk|wmv|pptx|flv)$',
                'domain':'',
                'crossdomain':r'(https?|http):\/\/'
            },
        'headers':{
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            #"cookie": "",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
            },
        'whitelist_file':'./config/url_whitelist.txt',
        'key_words':['百度'],
        'proxies':{
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080",
                },
        'scan_plug_in_unit':['BaiduSpider'],
        'baidu_words':[''],#,'赌','彩','在线','荷官'],
        'Spider_UA' : {
            'baidu':'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,likeGecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)',
            'baidu_yd':'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            'firefox_macos':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:79.0) Gecko/20100101 Firefox/79.0",
            #'360_safe':"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17",
            #'Android':"Mozilla/5.0 (Linux; Android 9; MI 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.105 Mobile Safari/537.36",
            },

}

