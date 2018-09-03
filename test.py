from Tkinter import *
import os
FONTSIZE = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 26, 28, 36, 48, 72,
            "初号", "小初", "一号", "小一", "二号", "小二", "三号", "小三",
            "四号", "小四", "五号", "小五", "六号", "小六", "七号", "八号"]
def getSysFonts():
    path=r"C:\Windows\Fonts"
    fonts_files = os.listdir(path)
    # print fonts_files
    fonts = []
    for fonts_file in fonts_files:
        if fonts_file.endswith(".TTF") or fonts_file.endswith(".ttf"):
            fonts.append(fonts_file[:fonts_file.rfind(".")])
    return fonts

def selectFont(event):
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    entry_font.delete(0, END)
    entry_font.insert(END, value)

def selectStyle(event):
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    entry_style.delete(0, END)
    entry_style.insert(END, value)

def selectFontsize(event):
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    entry_fontsize.delete(0, END)
    entry_fontsize.insert(END, value)

root = Tk()
root.title("字体")
root.resizable(width=False,height=False)

frame_font = Frame(root)
label_font = Label(frame_font, text="字符(F):")
label_font.pack(side=TOP, fill=X)
entry_font = Entry(frame_font)
entry_font.pack(side=TOP, fill=X, expand=True)
scrollbar_font = Scrollbar(frame_font, orient=VERTICAL)
listbox_font = Listbox(frame_font, yscrollcommand=scrollbar_font.set, selectmode=EXTENDED)
scrollbar_font.config(command=listbox_font.yview)
scrollbar_font.pack(side=RIGHT, expand=True, fill=Y)
fonts = getSysFonts()
for font in fonts:
    listbox_font.insert(END, font)
listbox_font.bind("<Double-Button-1>", selectFont)
listbox_font.pack(side=LEFT)
# frame_font.pack(side=LEFT, padx=10, pady=10)
frame_font.grid(row=0, column=0, sticky=NW, padx=10, pady=10)
# frame_font.pack()

frame_style = Frame(root)
label_style = Label(frame_style, text="字形(Y):")
label_style.pack(side=TOP)
entry_style = Entry(frame_style)
entry_style.pack(side=TOP, fill=X, expand=True)
scrollbar_style = Scrollbar(frame_style, orient=VERTICAL)
listbox_style = Listbox(frame_style, yscrollcommand=scrollbar_style.set, selectmode=EXTENDED)
scrollbar_style.config(command=listbox_style.yview)
scrollbar_style.pack(side=RIGHT, expand=True, fill=Y)
listbox_style.pack(side=LEFT)
for style in ["常规", "倾斜", "粗体", "粗偏斜体"]:
    listbox_style.insert(END, style)
listbox_style.bind("<Double-Button-1>", selectStyle)
# frame_style.pack(side=TOP, padx=10, pady=10)
listbox_style.select_set(0)
frame_style.grid(row=0, column=1, sticky=N, padx=10, pady=10)

frame_fontsize = Frame(root)
label_fontsize = Label(frame_fontsize, text="大小(S):")
label_fontsize.pack(side=TOP)
entry_fontsize = Entry(frame_fontsize)
entry_fontsize.pack(side=TOP, fill=X, expand=True)
scrollbar_fontsize = Scrollbar(frame_fontsize, orient=VERTICAL)
listbox_fontsize = Listbox(frame_fontsize, yscrollcommand=scrollbar_fontsize.set, selectmode=EXTENDED)
scrollbar_fontsize.config(command=listbox_fontsize.yview)
scrollbar_fontsize.pack(side=RIGHT, expand=True, fill=Y)
listbox_fontsize.pack(side=LEFT)
# frame_fontsize.pack(side=RIGHT, padx=10, pady=10)
for fs in FONTSIZE:
    listbox_fontsize.insert(END, fs)
listbox_fontsize.bind("<Double-Button-1>", selectFontsize)
listbox_fontsize.select_set(FONTSIZE.index("小四"))
listbox_fontsize.see(FONTSIZE.index("小四"))
frame_fontsize.grid(row=0, column=2, sticky=NE, padx=10, pady=10)

# lb_font_style = Label(text="字形(Y):")
# lb_font_style.pack(side="top")

root.mainloop()


