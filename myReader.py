import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import re
import tkinter.scrolledtext as ts
import pickle as pk


'''功能打开文档，翻页功能（视情况是否保存历史数据）hhhhh'''

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
        if not (filename in historyList):
            historyList.append(filename)
            if historyList.__len__() > 5:
                historyList.pop(0)
            saveHistoryFileName()
        else:
            historyList.remove(filename)
            historyList.append(filename)
            saveHistoryFileName()
        #重置文件路径的名称
        file_path.set(filename)
        #filePathLabel.config(text = filename)
        #重置按钮的位置
        initHistoryButtonCommand()
        with open(filename,'r',encoding = 'UTF-8') as f:
            content = f.readlines()
        insertText(setting.get())
# 获取一页（默认20行的内容）
#插入数据的代码过多，组成一个函数吧
def insertText(information):
    global text
    text.config(state=tk.NORMAL)
    text.delete(0.0, tk.END)
    text.insert(tk.INSERT, getOnePage(information))
    text.config(state=tk.DISABLED)
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
        pg = getOnePage(lines)
        insertText(pg)
    else:
        nowPage = 0
        pg = getOnePage()
        insertText(pg)
        
#按钮的方法跳转
def skipPage():
    global entry
    global nowPage
    for i ,v in enumerate(content):
        if v.find(entry.get())!= -1 :
            nowPage = i
            insertText(setting.get())
            break
        elif i+1 == content.__len__():
            mb.showinfo('WORNING!','Not found worlds in text file')
def nextSection():
    global nowSection
    global nowPage
    oneSectionPages = 300
    begin = nowPage - int(setting.get()) + 1
    end = begin + oneSectionPages
    key = ''
    tem = ''
    for i in range(begin,end):
        if i < content.__len__():
            tem += content[i]
    sections = re.findall(r'第\d{1,5}章',tem)
    print(sections)
    if sections.__len__() != 0:
        key = sections[0]
        keys = int(re.search(r'\d{1,5}',key).group())
        toMatch = '第'+ str(keys) + '章'
        for i ,v in enumerate(content):
            if v.find(toMatch)!= -1 :
                nowPage = i
                insertText(setting.get())
                break
            elif i+1 == content.__len__():
                mb.showinfo('WORNING!','Not found worlds in text file')
    else :
        mb.showinfo('WORNING!','Not found keyWorld 第N章 in text file')   
        
    
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
    #command 引用的变量 ，参数又引用变量，导致最后引用的都是同一个变量。
    #所以button不起变化啊啊啊啊（变量的理解不深刻）
    global btList
    #似乎找到了解决的方式：_value = value
    for i ,value in enumerate(historyList):
        btList[i].config(command = lambda _value = value : getText(openByAskOrFilepath = _value))
    '''
    v1,v2,v3,v4,v5 = historyList[0],historyList[1],historyList[2],historyList[3],historyList[4]
    btList[0].config(command = lambda : getText( openByAskOrFilepath = v1))
    btList[1].config(command = lambda : getText( openByAskOrFilepath = v2))
    btList[2].config(command = lambda : getText( openByAskOrFilepath = v3))
    btList[3].config(command = lambda : getText( openByAskOrFilepath = v4))
    btList[4].config(command = lambda : getText( openByAskOrFilepath = v5))
    '''
    print(historyList)
    if 'INIT' in historyList:
        #先取消安装
        for i in range(5):
            btList[i].pack_forget()
    #再次安装
    for i in range(5):
        if historyList[i] !='INIT':
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
text.pack(side = 'top',fill = tk.BOTH,pady = 5)


#开启F2 界面的历史记录

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
