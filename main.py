#coding:utf-8
from tkinter import *
from weiboSpider.spiders.weibo_spider import Start

#爬虫程序入口
class Application(Frame):
    def __init__(self, master=None,):
        Frame.__init__(self, master)
        self.pack()  # 把Widget加入到父容器中，并实现布局
        self.create_widgets()
        self.weibostart=Start()

    def create_widgets(self):
        self.choose = IntVar()

        self.welcomeLabel = Label(self, font=("宋体", 25, "bold"), text="欢迎进入微博爬虫系统", compound=CENTER)
        self.welcomeLabel.pack()

        self.keywordLabel = Label(self, font=('Helvetica', '15', 'bold'), text='请输入爬取微博的关键字')
        self.keywordLabel.pack()
        self.keywordInput = Entry(self)
        self.keywordInput.pack()

        self.pageLabel = Label(self, font=('Helvetica', '15', 'bold'), text='请输入爬取页数（共100页）')
        self.pageLabel.pack()
        self.pageInput = Entry(self)
        self.pageInput.pack()

        self.allfan1 = Label(self, font=('Helvetica', '15', 'bold'), text='是否按关键词爬取粉丝微博信息（请输入1或0）')#如果选择否将爬取粉丝所有微博
        self.allfan1.pack()
        self.allfan = Label(self, font=('Helvetica', '10', 'bold'), text='（1表示是,0表示否)如果选择否将爬取粉丝所有微博')
        self.allfan.pack()
        self.allfanInput = Entry(self)
        self.allfanInput.pack()

        self.fanpageLabel = Label(self, font=('Helvetica', '15', 'bold'), text='请输入爬取粉丝页数')
        self.fanpageLabel.pack()
        self.fanpageInput = Entry(self)
        self.fanpageInput.pack()

        self.TimestartLabel=Label(self, font=('Helvetica', '15', 'bold'), text='请输入爬取粉丝微博内容发布开始时间：（20130202）')
        self.TimestartLabel.pack()
        self.TimestartInput = Entry(self)
        self.TimestartInput.pack()

        self.TimeendLabel = Label(self, font=('Helvetica', '15', 'bold'), text='请输入爬取粉丝微博内容发布结束时间：（20170812)')
        self.TimeendLabel.pack()
        self.TimeendInput = Entry(self)
        self.TimeendInput.pack()

        self.Crawlbutton = Button(self, text='开始爬取', font=("Helvetica", 20, "bold"), command=self.begin)
        self.Crawlbutton.pack()

    def begin(self):
        top = Toplevel(self)
        scnWidth, scnHeight = root.maxsize()
        tmpcnf = '%dx%d+%d+%d' % (300, 120, (scnWidth - 800) / 2, (scnHeight - 400) / 2)
        top.geometry(tmpcnf)

        # 获取输入关键字和爬去页数
        fan_page = self.fanpageInput.get().encode('utf-8')
        page = self.pageInput.get().encode('utf-8')
        timestart=self.TimestartInput.get().encode('utf-8')
        timeend=self.TimeendInput.get().encode('utf-8')
        allfan=self.allfanInput.get().encode('utf-8')
        if page is None or fan_page == b'' or allfan is None:
            self.label1 = Label(top, font=('Helvetica', '15', 'bold'), text='请输入正确信息！')
            self.label1.pack()
        elif allfan == '1' and timeend is None or timestart is None:
            self.label1 = Label(top, font=('Helvetica', '15', 'bold'), text='搜索开始时间和结束时间！')
            self.label1.pack()
        else:
            try:
                page_num= int(self.pageInput.get().encode('utf-8'))#爬取页数
                fan_page = int(self.fanpageInput.get().encode('utf-8'))#爬取粉丝页数
                keyword = str(self.keywordInput.get())#关键词
                allfan = int(allfan)  # 是否按关键词爬取粉丝微博标志
                if allfan==1:
                    timeend=int(timeend)#粉丝微博结束时间
                    timestart=int(timestart)#粉丝微博开始时间
                else:
                    timeend = None  # 粉丝微博结束时间
                    timestart = None  # 粉丝微博开始时间

            except Exception as e:
                print(e)
                self.label2 = Label(top, font=('Helvetica', '15', 'bold'), text='请输入正确信息！')
                self.label2.pack()
                return
            self.weibostart.start(keyword,fan_page,page_num,allfan,timestart,timeend)#调用start启动爬虫程序,传递参数

root = Tk()
# 设置窗口大小
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry('800x500')

app = Application()
# 设置窗口标题:
app.master.title('ScrapySpider')

# 主消息循环:
app.mainloop()