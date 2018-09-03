import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser
import re
import tkinter.scrolledtext as ts
import pickle as pk
from  requests import post
from bs4 import BeautifulSoup as bs


'''功能打开文档，翻页功能 （视情况是否保存历史数据）hhhhh
https://www.biqugexsw.com/31_31690/11602024.html
'''

#获取某个文件的内容，初始化 content ，把第一页的内容赛进text

def getText(openByAskOrFilepath = 'byAsk'):
    global content
    global nowPage
    global historyList
    nowPage = 0
    if openByAskOrFilepath == 'byAsk':  
        filename = fd.askopenfilename()
    else:
        filename = openByAskOrFilepath
        print('打开的文件是：',filename)
    if filename != '':
        addToHistoryFile(filename)
        #重置文件路径的名称
        file_path.set(filename)
        #filePathLabel.config(text = filename)
        #重置按钮的位置
        initHistoryButtonCommand()
        try :
            
            with open(filename,'r') as f:
                content = f.readlines()
                
        except UnicodeDecodeError:
            print(f.encoding,'打开文件失败，试用utf-8打开')
            try:
                with open(filename,'r',encoding = 'UTF-8') as f:
                    content = f.readlines()
            except:
                print(f.encoding,'打开文件失败，弹出提示！')
                mb.showerror('文件打开错误','请检查打开文件是否有误！')
                
        
        insertText(setting.get())
# 获取一页（默认20行的内容）
#插入数据的代码过多，组成一个函数吧
def insertText(pages):
    global text
    text.config(state=tk.NORMAL)
    text.delete(0.0, tk.END)
    text.insert(tk.INSERT, getOnePage(pages))
    text.config(state=tk.DISABLED)
#抽象显示通过网页访问的方式
def showInternationPage(url):
    global text
    global nextPageUrl
    global content
    host = re.findall('^.*com',url)[0]
    response = post(url)
    result = response.text
    soup = bs(result,'html.parser')
    myContent = str(soup.find(id = 'content').text).replace('<br/>','\n')
    #去广告
    myContent = myContent.replace(url+'　　请记住本书首发域名：www.biqugexsw.com。笔趣阁小说网手机版阅读网址：m.biqugexsw.com','')
    '''
    content = myContent.split('\n')
    print(content.__len__())
    insertText(setting.get())
    '''
    text.config(state=tk.NORMAL)
    text.delete(0.0, tk.END)
    text.insert(tk.INSERT, myContent)
    text.config(state=tk.DISABLED)

    #获取名称and显示名称
    title = soup.find('title').text
    file_path.set(title)
    #为下一章做准备
    a_list = soup.find_all('a')
    for a in a_list:
        if a.text == '下一章':
            nextPageUrl = host + a.get('href')
            print(nextPageUrl)
            break
    #添加到历史记录
    addToHistoryFile(url)
    entryContent.set(url)
#添加到历史记录(仅仅修改history和save到本地)
def addToHistoryFile(fileName):
    global historyList
    if fileName in historyList:
        historyList.remove(fileName)
        historyList.append(fileName)
        saveHistoryFileName()
        
    else:
        historyList.append(fileName)
        if historyList.__len__() > 5:
            historyList.pop(0)
            saveHistoryFileName()
        
    #print('addToHistoryFile',historyList)
def getOnePage(lines = 20):
    global content
    global nowPage
    #print(lines,type(lines))
    lines = int(lines)
    tem = ''
    times = 0 
    if lines < 0:
        begin = nowPage + 2*lines
        end = nowPage +lines
    else :
        begin = nowPage
        end = nowPage + lines
    
    for i in range(begin,end):
        if i < content.__len__():
            tem += content[i]
            times += 1
        else :
            break
    if lines < 0:
        nowPage -= times
    else:
        nowPage += times
    #print ('nowPage',nowPage,tem)
    return tem
#按钮的方法下一页
def nextPage():
    lines = setting.get() 
    if nowPage  < content.__len__():
        insertText(setting.get())
#按钮的方法上一页
def previouPage():
    global nowPage
    lines = int(setting.get())*-1
    if nowPage + lines > 0:
        insertText(lines)
    else:
        nowPage = 0
        insertText(-lines)

    
    
#按钮的方法跳转
def skipPage(skipToEntryORInput = 'entry'):
    global text
    global entry
    global nowPage
    global nextPageUrl
    global host
    if skipToEntryORInput == 'entry':
        seachContent=entry.get()
    else:
        seachContent= skipToEntryORInput
    if 'http' in seachContent:
        url = seachContent
        showInternationPage(url)
        #重置按钮的功能
        initHistoryButtonCommand()
    else:
        for i ,v in enumerate(content):
            if v.find(seachContent)!= -1 :
                nowPage = i
                insertText(setting.get())
                break
            elif i+1 == content.__len__():
                mb.showinfo('WORNING!','Not found worlds in text file')
def nextSection():
    global nowSection
    global nowPage
    global nextPageUrl
    global host
    oneSectionPages = 300
    begin = nowPage - int(setting.get()) + 1
    end = begin + oneSectionPages
    key = ''
    tem = ''
    seachContent=entry.get()
        #线上版
    if 'http' in seachContent:
        showInternationPage(nextPageUrl)
        #保存到历史记录文件
        addToHistoryFile(nextPageUrl)
        #重置按钮的位置
        initHistoryButtonCommand()
    else:
        #线下版
        for i in range(begin,end):
            if i < content.__len__():
                tem += content[i]
        sections = re.findall(r'第.{1,5}章',tem)
        print(sections)
        if sections.__len__() != 0:
            key = sections[0]
            for i ,v in enumerate(content):
                if v.find(key)!= -1 :
                    nowPage = i
                    insertText(setting.get())
                    break
                elif i+1 == content.__len__():
                    mb.showinfo('WORNING!','Not found worlds in text file')
        else:
            mb.showinfo('WORNING!','Not found keyWorld 第N章 in text file') 
#设置text 的背景颜色               
def setTextColor():
    global text
    bgc = tkinter.colorchooser.askcolor()
    text.config(bg = bgc[1])
    print('设置背景颜色：',bgc[1])
    
#工具类函数，存和取
def saveHistoryFileName():
    global historyList
    with open('history.pkl','wb') as f :
        pk.dump(historyList,f)
def loadFile():
    historyInfo = []
    try :
        
        with open('history.pkl','rb') as f: 
            historyInfo = pk.load(f)
    except :
        historyInfo = ['INIT']*5
        
    return historyInfo
    
def initHistoryButtonCommand():
    #负责初始化按钮的名称和调整text内容的作用
    
    #command 引用的变量 ，参数又引用变量，导致最后引用的都是同一个变量。
    #所以button不起变化啊啊啊啊（变量的理解不深刻）
    #似乎找到了解决的方式：_value = value
    global btList
    for i ,value in enumerate(historyList):
        if 'http' in value:
            btList[i].config(command = lambda _value = value :skipPage(skipToEntryORInput = _value ))
        else:
            btList[i].config(command = lambda _value = value : getText(openByAskOrFilepath = _value))
    #print(historyList)
    #如果还未全部初始化完成就先取消安装
    if 'INIT' in historyList:
        for i in range(5):
            btList[i].pack_forget()
    #调整按钮名称的功能
    #判断是否是http模块
    for i in range(5):
        if historyList[i] !='INIT':
            if 'http' in historyList[i]:
                btList[i].config(text = historyList[i])
                btList[i].pack(padx=5, fill=tk.X ,side = 'bottom')
            else:
                btList[i].config( text= (re.search('\/.*$', historyList[i]).group().split('/')[-1]))
                btList[i].pack(padx=5, fill=tk.X ,side = 'bottom')

            
    
root = tk.Tk()
root.title('reader_have_fun')
root.geometry('600x500')
#初始化全局变量
content = []
nowPage = 0
nowSection = 0
historyList = loadFile()
initPageNumber = 20
nextPageUrl = ''
#准备添加历史记录功能，增加两个大frame，F1，F2
F1 = tk.Frame(root)
F2 = tk.Frame(root)
# settingFrame 和 seting框
settingFrame = tk.Frame(F1)
textVar = tk.Variable()
textVar.set(initPageNumber)
setting = tk.Entry(settingFrame,width = 4 , bd = 4 ,textvariable = textVar)
#打开的按钮
bt_open = tk.Button(settingFrame,text = 'openFile')
bt_open.config(command = getText)
#下一章节按钮
bt_section = tk.Button(settingFrame,text = 'nextSection')
bt_section.config(command = nextSection)
#安装bt_open 和seting 框 和下一章按钮
bt_open.pack(side = 'left',padx = 5)
setting.pack(side = 'left',padx = 5)
bt_section.pack(side = 'left',padx =5)

# 框架1 翻页,跳转功能
frm = tk.Frame(F1)
bt_nextPage = tk.Button(frm,text = 'nextPage',command = nextPage)
entry = tk.Entry(frm , bd = 3 , width = 30 )
entryContent = tk.StringVar()
entryContent.set('you can search')
entry.config(textvariable = entryContent)
bt_skipPage = tk.Button(frm,text = 'skip to ',command = skipPage)
bt_beforePage = tk.Button(frm, text = 'previouPage',command = previouPage)
widget_padx = 5
bt_beforePage.pack(side = 'left',padx = widget_padx)
entry.pack(side = 'left',padx = widget_padx )
bt_skipPage.pack(side = 'left',padx = widget_padx)
bt_nextPage.pack(side = 'left',padx = widget_padx)
#退出按钮
bt_exit = tk.Button(F1,text = 'quit',command = root.destroy)
#安装各个控件
bt_exit.pack(side ='bottom')
frm.pack(side = 'bottom')
settingFrame.pack(side = 'bottom')
#增加label显示文件路径
#filePathLabel = tk.Label(F1,justify = 'right')
filePathLabel = tk.Entry(F1,justify = 'left',width = 68)#,state = tk.DISABLED)
file_path = tk.StringVar()
file_path.set('还没打开文件哦~')
filePathLabel.config(textvariable = file_path)
filePathLabel.pack(side = 'top',pady = 5 )
#文本框展示内容&加个滚动条
text = ts.ScrolledText(F1,width = 68,height = 30 )
#text.config(bg = 'silver')
text.pack(side = 'top',fill = tk.BOTH,pady = 5)

#开启F2 界面的历史记录
#设置颜色，之后可能开辟菜单，放入菜单中
colorChooseBt = tk.Button(F2,text = 'setBgColor',command = setTextColor)
colorChooseBt.pack(side = tk.TOP, pady = 50)
#f2的名称
f2Title = tk.Label(F2,text = 'history recode')
f2Title.pack(side = tk.TOP,fill = tk.X)
#搞个frame装4个button
historyListFrame = tk.Frame(F2)
btList = [0]*5
#初始化5个button
for i in range(5):
     btList[i] = tk.Button(historyListFrame)
initHistoryButtonCommand()
for i,value in enumerate(historyList):
    if value !='INIT':
        btList[i].config( text= (re.search('\/.*$', value).group().split('/')[-1]))
        btList[i].pack(padx=5, fill=tk.X ,side = 'bottom')
historyListFrame.pack()
#两个大框架的安装
    
F1.pack(side = 'left',padx = 5)
F2.pack(side ='left', padx = 5)

root.mainloop()
