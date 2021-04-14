import re
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.41"
}
#获取网页源代码
def get_html(url):
    try:
        res= requests.get(url,headers=headers)
        return res.text
    except:
        return ""

#获取子url列表
def get_son_url(url):
    # 获取
    html = get_html(url)

    html_re = '<a href="([a-zA-z]+://[^\s]*)"'
    href_list = re.findall(html_re,html,re.S)
    return href_list
#广度爬取
def vast_path(url):
    #队列方法   先进先出
    #append 入队列  pop 出队列  用列表 模拟队列
    num = 0
    url_queue = []
    url_queue.append(url) #默认先把第一个放进来

    while len(url_queue)>0:
        #出队列 每次取出一个
        url = url_queue.pop(0)
        print("\t",'当前层级:%d'%deepdict[url],url)
        getscript(url,num)
        num = num+1

        if deepdict[url]<2:
            #获取子url列表
            sonurl_list = get_son_url(url)
            for sonurl in sonurl_list:
                #过滤出有效链接
                if sonurl.startswith('https') or sonurl.startswith('http'):
                    if sonurl not in deepdict: #过滤重复url
                        deepdict[sonurl] = deepdict[url]+1
                        #入队列
                        url_queue.append(sonurl)

#处理外部脚本
def outscript(scripturl,num,num1):
    if(scripturl[0]=='/' and scripturl[1]=='/'):
        url = 'https:'+scripturl
    else:
        if(scripturl[0]=='h'):
            url = scripturl
        else:
            print("Something is wrong!")
            return
            # url = 'https://'+scripturl

    # print(url)
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    res = s.get(url) # 你需要的网址
    result = res.text
    #写入文件
    filename = 'C://Users/Wsy/Desktop/testforspider/Outside/script %(num)d %(num1)d.txt' %{"num":num,"num1":num1}
    with open (filename,'w',encoding='utf-8') as file_object:
        file_object.write(result)

#获取标签为<script>的元素，并将其分类后处理
def getscript(url,num):
    num1 = 0
    num2 = 0
    #获取
    requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
    s = requests.session()
    s.keep_alive = False # 关闭多余连接
    r = s.get(url) # 你需要的网址
    re = r.text
    #print(re)
    #解析
    soup = BeautifulSoup(re,"html.parser")
    #打印
    # print(soup)
    # print(soup.prettify())
    # 内含脚本文件链接的元素
    results = soup.findAll('script',{"src":True})
    for result in results:
        # 外部脚本
        resultout = str(result['src'])
        if(resultout[0]!='/' and resultout[0:4]!='https'):
            resultout = url+resultout
        else:
            if(resultout[0]=='/' and resultout[1]!='/'):
                resultout = url+'/'+resultout
        outscript(resultout,num,num1)
        print(resultout)
        num1 = num1+1
        # 内嵌脚本
    results = soup.findAll('script',{"src":False})
    for result in results:
        text = result.string
        filename = 'C://Users/Wsy/Desktop/testforspider/Inside/script %(num)d %(num1)d.txt' %{"num":num,"num1":num1}
        with open (filename,'w',encoding='utf-8') as file_object:
            file_object.write(text)


if __name__ == '__main__':
    url = 'https://www.jd.com'
    # 控制层级

    deepdict = {} #控制层级
    deepdict[url] = 1 # 默认第一级

    vast_path(url)

