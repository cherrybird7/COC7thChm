import os
import codecs
import tkinter as tk
from tkinter import filedialog

PREFIX = """[GENERAL]
Ver=1
Title=COC7th 不全书
RootDir=
Dictionary=en_US
DefaultTopic=写在前面.htm
CompiledFile=<Project_Folder>_output\HTML Help\试做COC残缺大典原始版本 (2).chm
CustomTemplate=<Project_Folder>\模板\空白页模板.htm
DefaultTemplate=0
Language=0x0804
Encoding=gb2312
DeleteProject=0
ViewCompiledFile=0
HasChild=0
NoChild=10
HtmlHelpTemplate=
HtmlHelpTitle=COC7th 不全书
HtmlHelpTitleSame=1
HtmlHelpOutputEncoding=gb2312
WebHelpDefault=写在前面.htm
WebHelpOutputFolder=<Project_Folder>_output\Web Help\
WebHelpTemplate=
WebHelpTitle=COC7th 不全书
WebHelpDefaultSame=1
WebHelpTemplateSame=1
WebHelpTilteSame=1
WebHelpLanguage=1
StartFromRoot=1
AutoCollapse=0
DrawLines=1
SingleHtmlFilename=试做COC残缺大典原始版本 (2).htm
SingleHtmlOutputFolder=<Project_Folder>_output\SingleHTML\
SingleHtmlTitle=COC7th 不全书
SingleHtmlHasToc=0
SingleHtmlSame=1
WordFileTitle=COC7th 不全书
WordFileTitleSame=1
WordFile=<Project_Folder>_output\WordDoc\a.docx
PDFfile=<Project_Folder>_output\PDF\a.pdf
HeadProperties=1
PageProperties=1
RealColorIcon=0
ShowIndex=1
NavWidth=270
WebFontColor=#DBEFF9
WebBackColor=
WebBackground=1
HHPFolder=

[CHMSetting]
Top=50
Left=50
Height=500
Width=700
PaneWidth=270
DefaultTab=0
ShowMSDNMenu=0
ShowPanesToolbar=1
ShowPane=1
HideToolbar=0
HideToolbarText=0
StayOnTop=0
Maximize=0
Hide=1
Locate=1
Back=1
bForward=1
Stop=1
Refresh=1
Home=1
Print=1
Option=1
Jump1=0
Jump2=0
AutoShowHide=0
AutoSync=1
Content=1
Index=1
Search=1
Favorite=1
UseFolder=0
AutoTrack=0
SelectRow=0
PlusMinus=1
ShowSelection=1
ShowRoot=1
DrawLines=1
AutoExpand=0
RightToLeft=0
LeftScroll=0
Border=0
DialogFrame=0
RaisedEdge=0
SunkenEdge=0
SavePosition=0
ContentsFont=,8,0
IndexFont=,8,0
Title=COC7th 不全书
Language=0x0804
Font=
DefaultTopic=写在前面.htm

[DocSetting]
PaperSize=4
Height=0
Width=0
Top=25
Bottom=25
Left=30
Right=30
Cover=1
Header=1
Footer=1
Toc=1
XE=0
ShowLevel=3
TOCCaption=Table of Contents
TitleNumber=1
AddHint=0
HintFormat=See [Title No.]
StartNewPage=0
Discard=1
Addenda=Addenda
Panes=0
Magnification=0
PageLayout=0

[TOPICS]
TitleList="""


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title="选择所用的文件夹（与工程目录之间取相对路径）",initialdir=r"../")
    if file_path != None:
        relative_file_path = os.path.relpath(file_path,"../")
        print("文件夹地址：./"+file_path)
        wcp_name = os.path.basename(file_path)
        print("wcp名称："+wcp_name+"_生成.wcp")
        object_list = []
        for folder, dirs, files in os.walk(file_path):
            folder_name = os.path.basename(folder)
            relative_path = os.path.relpath(folder,"../")
            depth = relative_path.count("/")+relative_path.count("\\")
            object_list.append([folder_name,"",depth])
            #print(folder_name + ":" + str(files))
            for name in files:
                object_list.append([name.split('.')[0],os.path.relpath(os.path.join(folder,name),"../"),depth+1])
        #print(object_list)
        object_str_list = []
        index = 0
        for object_data in object_list:
            object_str_list.append("TitleList.Title."+str(index)+"="+object_data[0]+"\nTitleList.Level."+str(index)+"="+str(object_data[2])+"\nTitleList.Url."+str(index)+"="+object_data[1]+"\nTitleList.Status."+str(index)+"=0\nTitleList.Keywords."+str(index)+"=\nTitleList.ContextNumber."+str(index)+"="+str(index+1000)+"\nTitleList.ApplyTemp."+str(index)+"=0\nTitleList.Expanded."+str(index)+"=0\nTitleList.Kind."+str(index)+"=0")
            index += 1
        
        with open("../"+wcp_name+"_生成.wcp",'wb') as _f:
            _f.write(codecs.BOM_UTF16_LE)
            _f.write((PREFIX + str(len(object_list))).encode('utf-16-le'))
            for object_str in object_str_list:
                _f.write(("\n"+object_str).encode('utf-16-le'))
        print("已完成制作！")
    else:
        print("已取消")