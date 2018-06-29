#coding:utf-8

from weiboSpider.items import WeibospiderItem,FanItem
from scrapy.crawler import CrawlerProcess
import scrapy
from tkinter import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request, FormRequest
from bs4 import BeautifulSoup
import urllib
from scrapy.utils.project import get_project_settings
import datetime
import time
class weibospider(scrapy.Spider):
    name="weibo"
    allowed_domains = ["weibo.com","weibo.cn"]
    #请求登录
    def start_requests(self):
        url='https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn'
        return [Request(url=url,meta={'cookiejar':1},callback=self.start_login)]
    #向服务器提交登录请求
    def start_login(self,response):
        # #帐号，密码
        username = ""
        password = ""
        try:
            return [FormRequest('https://passport.weibo.cn/sso/login',method='POST',meta={'cookiejar':response.meta['cookiejar']},formdata={'password':
password,'username':username},callback=self.afterlogin)]
        except Exception as e:
            print(e,"登录失败！")

    #关键词搜索
    def afterlogin(self,response):
        try:
            self.logger.info(str(response.meta['cookiejar']))
            # 根据输入要爬取的页数进行循环处理
            for T_num in range(1, page_num + 1):
                print('正在爬取关键词搜索第%s页内容' % T_num)
                num_page = str(T_num)
                urlnext = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=' + keyword + '&page=' + num_page
                yield scrapy.Request(url=urlnext, meta={'cookiejar': response.meta['cookiejar']},callback=self.afterparse)
        except Exception as e:
            print(e,"登录失败！ ")

    #对关键词搜索内容进行处理
    def afterparse(self,response):
        """ 抓取微博数据 """
        try:
            soup=BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
            c_list=soup.find_all('div', id=re.compile(r'M'))
            if len(c_list)==0:
                return
            #该页关键词搜索微博内容
            for i in range(len(c_list)):
                id=c_list[i].find('a', class_="nk")
                if id is None:
                    return
                username=id.get_text()#用户名
                print(username)
                content=c_list[i].find('span',class_="ctt").get_text()#微博内容
                #从url中提取用户id
                print(content)
                url_content=c_list[i].find('a',class_="nk")
                url=url_content['href']
                if url is None:
                    return None
                allfanurl.append(url)
                uid_content = url.split('/')
                uid = uid_content[len(uid_content) - 1]#用户id
                all_num1=c_list[i].find('a',href=re.compile(r'https://weibo.cn/attitude'))
                comment=all_num1.get_text().split('[')[1].split(']')[0]#点赞数
                all_num2=c_list[i].find('a',href=re.compile(r'https://weibo.cn/repost.'))
                to_num=all_num2.get_text().split('[')[1].split(']')[0]#转发数
                all_num3 = c_list[i].find('a', href=re.compile(r'https://weibo.cn/comment.'))
                to_agree = all_num3.get_text().split('[')[1].split(']')[0]  # 评论数
                #获取微博发布时间
                now = datetime.date.today()
                timecontent=c_list[i].find('span',class_="ct")
                timecontent1=timecontent.get_text().split(' ')[0]
                if '今天' in timecontent1:
                    to_time =str(now.year)+'年'+str(now.month)+'月'+str(now.day)+'日'
                elif '分钟前' in timecontent1:
                    to_time = str(now.year)+'年'+str(now.month)+'月'+str(now.day)+'日'
                else:
                    if '年' not in timecontent1:
                        to_time=str(now.year)+'年'+str(timecontent1)
                    else:
                        to_time=timecontent1

                item=WeibospiderItem(username=username,uid=uid,weibocontent=content,pinglun=comment,zhuanfa=to_num,dianzhan=to_agree,fabushijian=to_time)
                request=scrapy.Request(url=url,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse)
                request.meta['item']=item
                yield request

        except Exception as e:
            print(e,"at afterparse")


    #提取粉丝数量
    def parse(self,response):
        try:
            item=response.meta['item']
            usersoup=BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
            fannum_content=usersoup.find_all('a',href=re.compile(r'/\d+/fans'))
            fannum=fannum_content[0].get_text().split('[')[1].split(']')[0]#粉丝数
            item['fenshinum']=fannum
            allnum=usersoup.find('span',class_="tc")
            if allnum is not None:
                num=allnum.get_text().split('[')[1].split(']')[0]#微博数量
                item['allweibonum']=num
            idhref=usersoup.find('a',href=re.compile(r'/.+/info'))
            id=idhref['href']
            new_url = "https://weibo.cn" + id
            request = scrapy.Request(url=new_url, meta={'cookiejar': response.meta['cookiejar']},
                                     callback=self.info)
            request.meta['item'] = item
            yield request
        except Exception as e:
            print(e,"at parse")
    #提取用户信息
    def info(self,response):
        try:
            item = response.meta['item']
            soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
            all_content=soup.find_all('div',class_="c")
            all_content1=all_content[3].get_text()
            gendercontent=re.search(re.compile(r'性别:\w{1}'),all_content1)
            if gendercontent is not None:
                gender=gendercontent.group().split(':')[1]
                item['gender']=gender
            to_areacontent=re.search(re.compile(r'地区:\w{2}'),all_content1)
            if to_areacontent is not None:
                to_area=to_areacontent.group().split(':')[1]
                item['diqu']=to_area
            tagcontent=re.search(re.compile(r'标签:\w{2,10}'),all_content1)
            if tagcontent is not None:
                tag=tagcontent.group().split(':')[1]
                item['biaoqian']=tag
            birthdaycontent=re.search(re.compile(r'生日:.{2,13}'),all_content1)
            if birthdaycontent is not None:
                birthday1=birthdaycontent.group().split(':')[1]
                birthday2=re.search(re.compile(r'\d{1,4}-\d{1,4}-{0,1}\d{1,4}'),birthday1)
                if birthday2 is not None:
                    birthday=birthday2.group()
                    item['birthday']=birthday
            introductioncontent=re.search(re.compile(r'简介:.{2,70}'),all_content1)
            if introductioncontent is not None:
                introduction=introductioncontent.group().split('简介:')[1].split('标签:')[0]
                item['jianjie']=introduction
            renzhengcontent=re.search(re.compile(r'认证信息:.{2,20}'),all_content1)
            if renzhengcontent is not None:
                renzheng=renzhengcontent.group().split('认证信息:')[1].split('简介:')[0]
                item['renzheng']=renzheng
            id=item['uid']
            yield item

            #按输入的页数循环爬取粉丝相关信息
            for f_num in range(1,fan_page+1):
                print('正在爬取第%s页粉丝'%f_num)
                f_num=str(f_num)
                new_url="https://weibo.cn/"+id+"/fans?page="+f_num
                request=scrapy.Request(url=new_url,meta={'cookiejar':response.meta['cookiejar']},callback=self.fanurlparser)
                yield request
        except Exception as e:
            print(e,"at info")
    #提取粉丝的url
    def fanurlparser(self,response):
        try:
            fansoup=BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')

            url_list=fansoup.find_all('a',href=re.compile(r'http://.*/u/\w'))
            if len(url_list)==0:
                return
                #该页粉丝url列表
            for i in range(len(url_list)):
                fanurl=url_list[i]['href']
                content=[]
                uid=fanurl.split('/')[-1]
                #去重粉丝url
                if fanurl not in allfanurl:
                    allfanurl.append(fanurl)
                    # 爬取所有微博
                    if allfan == 0:
                        print('爬取所有微博')
                        item = FanItem(uid=uid,content=content)
                        request = scrapy.Request(url=fanurl, meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.fancontant)
                        request.meta['item'] = item
                        yield request
                    # 按关键词爬取微博
                    elif allfan == 1:
                        item = FanItem(uid=uid,content=content)
                        url = "https://weibo.cn/" + uid + "/search?f=u&rl=0"
                        request = scrapy.Request(url=url, meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.select)
                        request.meta['item'] = item
                        yield request
        except Exception as e:
            print(e,"at fanurlparser")
    #按关键词搜索粉丝微博
    def select(self,response):
        try:
            item = response.meta['item']
            id = str(item['uid'])
            timeend1=str(timeend)
            timestart1=str(timestart)
            keyword1=str(keyword)
            print(timestart1,timeend1,keyword1)
            url="https://weibo.cn/"+id+"/profile"
            return [FormRequest(url=url,method='POST',meta={'cookiejar': response.meta['cookiejar'],'item':item},formdata={'advancedfilter':'1','endtime':timeend1,'hasori':'0','haspic':'0',
'keyword':keyword1,'smblog':'筛选','starttime':timestart1,'uid':id }, callback=self.fancontant)]
        except Exception as e:
            print(e,"at select")

    #爬取粉丝信息和微博内容
    def fancontant(self,response):
        try:

            item = response.meta['item']
            fancontentsoup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
            fanname = fancontentsoup.find('span', class_="ctt").get_text().split('\xa0')[0]
            fannum_content = fancontentsoup.find_all('a', href=re.compile(r'/\d+/fans'))
            fannum = fannum_content[0].get_text().split('[')[1].split(']')[0]  # 粉丝数
            item['fenshinum'] = fannum
            allnum = fancontentsoup.find('span', class_="tc")
            if allnum is not None:
                num = allnum.get_text().split('[')[1].split(']')[0]  # 微博数量
                item['allweibonum'] = num
            item['username']=fanname
            content=item['content']

            fan_content_list=fancontentsoup.find_all('div',id=re.compile(r'M'))
            if len(fan_content_list) ==0:
                return
            for i in range(len(fan_content_list)):
                fancontent = {}
                all_num1 = fan_content_list[i].find('a', href=re.compile(r'http://weibo.cn/attitude'))
                comment = all_num1.get_text().split('[')[1].split(']')[0]  # 点赞数
                fancontent['dianzhan']=comment
                #item['comment']=comment
                all_num2 = fan_content_list[i].find('a', href=re.compile(r'http://weibo.cn/repost.'))
                to_num = all_num2.get_text().split('[')[1].split(']')[0]  # 转发数
                #item['to_num']=to_num
                fancontent['zhuanfa']= to_num
                all_num3 = fan_content_list[i].find('a', href=re.compile(r'http://weibo.cn/comment.'))
                to_agree = all_num3.get_text().split('[')[1].split(']')[0]  # 评论数
                #item['to_agree']=to_agree
                fancontent['pinglun']=to_agree
                fan_content=fan_content_list[i].find('span',class_='ctt').get_text()
                now = datetime.date.today()
                timecontent = fan_content_list[i].find('span', class_="ct")
                timecontent1 = timecontent.get_text().split(' ')[0]
                if '今天' in timecontent1:
                    to_time = str(now.year) + '年' + str(now.month) + '月' + str(now.day) + '日'
                elif '分钟前' in timecontent1:
                    to_time = str(now.year) + '年' + str(now.month) + '月' + str(now.day) + '日'
                else:
                    if '年' not in timecontent1:
                        to_time = str(now.year) + '年' + str(timecontent1)
                    else:
                        to_time = timecontent1
                fancontent['fabushijian']=to_time
                fancontent['weibocontent']=fan_content
                content.append(fancontent)
                #item['to_time']=to_time
                id = item['uid']
                url = "https://weibo.cn/" + id+"/info"
                request = scrapy.Request(url=url, meta={'cookiejar': response.meta['cookiejar']},
                                         callback=self.faninfo)
                request.meta['item'] = item
                yield request
            nextpagetext = fancontentsoup.find('div', class_="pa").find_all('a')
            if len(nextpagetext)==0:
                return
            if nextpagetext[0].get_text()=='下页':
                urlfirst='https://weibo.cn'
                nexturl=nextpagetext[0]['href']
                new_url=urllib.parse.urljoin(urlfirst,nexturl)
                request=scrapy.Request(url=new_url,meta={'cookiejar':response.meta['cookiejar']},callback=self.fancontant)
                yield request
        except Exception as e :
            print(e,"at fancontent")


     # 获取粉丝资料信息

    def faninfo(self, response):
        try:
            item = response.meta['item']
            soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
            all_content = soup.find_all('div', class_="c")
            all_content1 = all_content[3].get_text()
            gendercontent = re.search(re.compile(r'性别:\w{1}'), all_content1)
            if gendercontent is not None:
                gender = gendercontent.group().split(':')[1]
                item['gender'] = gender
            to_areacontent = re.search(re.compile(r'地区:\w{2}'), all_content1)
            if to_areacontent is not None:
                to_area = to_areacontent.group().split(':')[1]
                item['diqu'] = to_area
            tagcontent = re.search(re.compile(r'标签:\w{2,10}'), all_content1)
            if tagcontent is not None:
                tag = tagcontent.group().split(':')[1]
                item['biaoqian'] = tag
            birthdaycontent = re.search(re.compile(r'生日:.{2,13}'), all_content1)
            if birthdaycontent is not None:
                birthday1 = birthdaycontent.group().split(':')[1]
                birthday2 = re.search(re.compile(r'\d{1,4}-\d{1,4}-{0,1}\d{1,4}'), birthday1)
                if birthday2 is not None:
                    birthday = birthday2.group()
                    item['birthday'] = birthday
            introductioncontent = re.search(re.compile(r'简介:.{2,70}'), all_content1)
            if introductioncontent is not None:
                introduction = introductioncontent.group().split('简介:')[1].split('标签:')[0]
                item['jianjie'] = introduction
            renzhengcontent = re.search(re.compile(r'认证信息:.{2,20}'), all_content1)
            if renzhengcontent is not None:
                renzheng = renzhengcontent.group().split('认证信息:')[1].split('简介:')[0]
                item['renzheng'] = renzheng
            yield item
        except Exception as e:
            print(e,"at faninfo")
#爬虫启动
class Start(object):
    def start(self,keyword1,fan_page1,page_num1,allfan1,timestart1,timeend1):
        global keyword
        global fan_page
        global page_num
        global allfan
        global timeend
        global timestart
        global allfanurl
        allfanurl=[]
        keyword=keyword1
        fan_page=fan_page1
        page_num=page_num1
        allfan=allfan1
        timeend=timeend1
        timestart=timestart1
        process = CrawlerProcess( get_project_settings())
        process.crawl(weibospider)
        process.start()
# if __name__=='__main__':
#     global keyword
#     global fan_page
#     global page_num
#     global allfan
#     global timeend
#     global timestar
#     global allfanurl
#     allfanurl=[]
#     keyword = '萨德'
#     fan_page = 1
#     page_num = 2
#
#     process = CrawlerProcess( get_project_settings())
#     process.crawl(weibospider)
#     process.start()