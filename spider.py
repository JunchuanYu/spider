#!/usr/bin/env python
# coding: utf-8

# In[3]:


import urllib
from bs4 import BeautifulSoup
import re


# In[4]:


# 1.爬取网页
# 2.逐一解析数据
# 3.保存数据

def ask_url(url):
    
#     用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器
#     本质上是高速浏览器，我们可以接收什么水平的文件内容
    headers={
    'Cookie':'douban-fav-remind=1; gr_user_id=4e7b8655-2b03-459c-9a48-479a7ef3cff3; __gads=ID=923819f6e37c5755-229ac26e53c40080:T=1603262141:RT=1603262141:S=ALNI_MYy_bCfr14fGGCvAknniGhhKGPVIQ; bid="FBnypFe9U1o"; __yadk_uid=HOj0Wb20HMv7HILnUfZozV5ZJEUCcskz; ll="108288"; dbcl2="231526008:/T54SQ0gGpc"; ck=OAh4; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1611729184%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=3a032f5f916076a1.1611729184.1.1611729184.1611729184.; _pk_ses.100001.4cf6=*; __utma=30149280.125111915.1611729184.1611729184.1611729184.1; __utmb=30149280.0.10.1611729184; __utmc=30149280; __utmz=30149280.1611729184.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1087461599.1611729184.1611729184.1611729184.1; __utmb=223695111.0.10.1611729184; __utmc=223695111; __utmz=223695111.1611729184.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'
    ,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    req=urllib.request.Request(url=url,headers=headers)
    
    html=''
    try:
        response=urllib.request.urlopen(req)
        html=response.read().decode('utf-8')
#         print(html)
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)
    return html


find_info={
    'link':re.compile(r'<a href="(.*?)">'),
    'img':re.compile(r'<img.*src="(.*?)"',re.S), #re.S忽略换行符
    'title':re.compile(r'<span class="title">(.*)</span>'),
    'score':re.compile(r'<span class="rating_num" property="v:average">(.*)</span>'),
    'judge':re.compile(r'<span>(\d*人评价)</span>'),
    'inq':re.compile(r'<span class="inq">(.*)</span>'),
    'bd':re.compile(r'<p class="">(.*?)</p>',re.S)
}

def get_data(baseurl):
    datalist=[]
    
    for i in range(10):
        url=baseurl+str(i*25)
        html=ask_url(url)
        
        soup=BeautifulSoup(html,'html.parser')
        print(soup.title,'第',i+1,'页')
        for i in soup.find_all('div',class_='item'):
            data=[]
            i=str(i)
#             print(i)
#             break
            link=re.findall(find_info['link'],i)[0]
            data.append(link)
            
            img=re.findall(find_info['img'],i)[0]
            data.append(img)
            
            title=re.findall(find_info['title'],i)
            if len(title)==2:
                chinese_title=title[0]
                data.append(chinese_title)
                other_title=title[1].replace('/','') #去掉/
                data.append(other_title)
            else:
                data.append(title)
                data.append(' ') #其他名留空
            
            score=re.findall(find_info['score'],i)[0]
            data.append(score)
            
            judge=re.findall(find_info['judge'],i)[0]
            data.append(judge)
            
            inq=re.findall(find_info['inq'],i)
            if inq!=0:
                inq=inq[0].replace('。','')
                data.append(inq)
            else:
                data.append(' ')
            
            bd=re.findall(find_info['bd'],i)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?',' ',bd)
            data.append(bd.strip()) #去掉前后空格
            
#             print(data)
            datalist.append(data)
    
#     print(datalist)            
    return datalist

# 得到指定的一个URL的网页内容
def save_data(save_dir):
    print('save...')


# In[5]:


def main():
    baseurl='https://movie.douban.com/top250?start=&filter='
#     html=ask_url(baseurl)
#     save_data(save_dir)
    data_list=get_data(baseurl)

if __name__=='__main__':
    main()


# In[ ]:




