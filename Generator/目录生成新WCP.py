import codecs

PREFIX = """[GENERAL]
Ver=1
Title=COC7th 不全书
RootDir=
Dictionary=en_US
DefaultTopic=写在前面.htm
CompiledFile=<Project_Folder>_output\hTML help\试做 COC 残缺大典原始版本.chm
CustomTemplate=<Project_Folder>\模板\空白页模板.htm
DefaultTemplate=0
Language=0x0804
Encoding=UTF-8
DeleteProject=0
ViewCompiledFile=0
hasChild=0
NoChild=10
htmlhelpTemplate=
htmlhelpTitle=COC7th 不全书
htmlhelpTitleSame=1
htmlhelpOutputEncoding=gb2312
WebhelpDefault=写在前面.htm
WebhelpOutputFolder=<Project_Folder>_output\Web help\
WebhelpTemplate=
WebhelpTitle=COC7th 不全书
WebhelpDefaultSame=1
WebhelpTemplateSame=1
WebhelpTilteSame=1
WebhelpLanguage=1
StartFromRoot=1
AutoCollapse=0
DrawLines=1
SinglehtmlFilename=试做 COC 残缺大典原始版本 (2).htm
SinglehtmlOutputFolder=<Project_Folder>_output\SinglehTML\
SinglehtmlTitle=COC7th 不全书
SinglehtmlhasToc=0
SinglehtmlSame=1
WordFileTitle=COC7th 不全书
WordFileTitleSame=1
WordFile=<Project_Folder>_output\WordDoc\a.docx
PDFfile=<Project_Folder>_output\PDF\a.pdf
headProperties=1
PageProperties=1
RealColorIcon=0
ShowIndex=1
NavWidth=270
WebFontColor=#DBEFF9
WebBackColor=
WebBackground=1
hhPFolder=

[ChMSetting]
Top=50
Left=50
height=500
Width=700
PaneWidth=270
DefaultTab=0
ShowMSDNMenu=0
ShowPanesToolbar=1
ShowPane=1
hideToolbar=0
hideToolbarText=0
StayOnTop=0
Maximize=0
hide=1
Locate=1
Back=1
bForward=1
Stop=1
Refresh=1
home=1
Print=1
Option=1
Jump1=0
Jump2=0
AutoShowhide=0
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
ContentsFont=,10,0
IndexFont=,10,0
Title=COC7th 不全书
Language=0x0804
Font=
DefaultTopic=写在前面.htm

[DocSetting]
PaperSize=4
height=0
Width=0
Top=25
Bottom=25
Left=30
Right=30
Cover=1
header=1
Footer=1
Toc=1
XE=0
ShowLevel=3
TOCCaption=Table of Contents
TitleNumber=1
Addhint=0
hintFormat=See [Title No.]
StartNewPage=0
Discard=1
Addenda=Addenda
Panes=0
Magnification=0
PageLayout=0

[TOPICS]
TitleList="""

name = input('请输入要生成的 wcp 文件名：')

def convert_html_to_ini():
    object_list = ""
    
    title_level_map = {
        'h1': 0,
        'h2': 1,
        'h3': 2,
        'h4': 3,
        'h5': 4,
        'h6': 5
    }



    # 输入的标题数据
    print("请右键贴上你的目录（回车两次结束输入）：")
    
    lines = []
    while True:
        line = input()
        if line.strip() == '':  # 结束输入
            break
        lines.append(line.strip())
    
    title_list = []
    index = 0  # 从 TitleList.Title.0(默认开头) 开始，如果要修改起始序号，请修改这里

    # 维护上一级和上上一级标题
    last_h1_title = None
    last_h2_title = None
    last_h2_index = 0  # h2 的当前序号
    last_h3_title = None
    h2_count = 0  # 用于跟踪 h2 的数量

    for line in lines:
        if line.startswith("<") and line.endswith(">"):
            tag = line[1:line.index(">")]  # 提取标签名称
            title = line[line.index(">") + 1:line.rindex("<")]  # 提取标题内容
            level = title_level_map.get(tag, None)

            if level is not None:
                # 根据标题级别更新上一级标题
                if level == 0:  # h1
                    last_h1_title = title
                    last_h2_title = None  # Reset last h2 when h1 is found
                    last_h3_title = None  # Reset last h3 when h1 is found
                    last_h4_title = None

                elif level == 1:  # h2
                    h2_count += 1  # 增加 h2 的数量
                    last_h2_title = title
                    last_h3_title = None  # Reset last h3 when h2 is found
                    last_h4_title = None

                elif level == 2:  # h3
                    last_h3_title = title
                    last_h4_title = None
                
                elif level == 3:  # h4
                    last_h4_title = title

                elif level == 4:  # h5
                    last_h5_title = title

                # 根据级别生成 URL
                # {h2_count}.代表第一级标题的序号，默认最上面的文件夹带有序号，如果最上面的文件夹不带序号，请删掉下方的{h2_count}.
                if level == 0:  # h1
                    url = f"{title}\{title}.htm"
                elif level == 1:  # h2
                    url = f"{last_h1_title}\{h2_count}.{title}\{title}.htm"
                elif level == 2:  # h3
                    url = f"{last_h1_title}\{h2_count}.{last_h2_title}\{title}.htm"
                elif level == 3:  # h4
                    url = f"{last_h1_title}\{h2_count}.{last_h2_title}\{last_h3_title}\{title}.htm"
                elif level == 4:  # h5
                    url = f"{last_h1_title}\{h2_count}.{last_h2_title}\{last_h3_title}\{last_h4_title}\{title}.htm"
                elif level == 5:  # h6
                    url = f"{last_h1_title}\{h2_count}.{last_h2_title}\{last_h3_title}\{last_h4_title}\{last_h5_title}\{title}.htm"
                
                # 添加 TitleList 信息
                title_list.append(f"TitleList.Title.{index}={title}")
                title_list.append(f"TitleList.Level.{index}={level}")
                title_list.append(f"TitleList.Url.{index}={url}")
                title_list.append(f"TitleList.Icon.{index}=0")
                title_list.append(f"TitleList.Status.{index}=0")
                title_list.append(f"TitleList.Keywords.{index}=")
                title_list.append(f"TitleList.ContextNumber.{index}={1000 + index - 9}")
                title_list.append(f"TitleList.ApplyTemp.{index}=0")
                title_list.append(f"TitleList.Expanded.{index}=1")
                title_list.append(f"TitleList.Kind.{index}=0")
                index += 1
                
                for item in title_list:
                    object_list += item + "\n"
          
    filename = (f"{name}.wcp") # 文件名
    prefixtext = PREFIX + str(index) + "\n" # 前缀信息

    ## 创建 wcp 文件
    try:
       with open("../"+filename,'wb') as _f:
           _f.write(codecs.BOM_UTF16_LE)
           _f.write((prefixtext + object_list).encode('utf-16-le'))
    except Exception as e:#如果出错，打印错误信息
       print(f"写入文件失败：{e}")

    print(f"\n{filename}已生成")
    input("请按任意键退出...")

# 调用函数
convert_html_to_ini()