import os
import math
import codecs
import tkinter as tk
from tkinter import filedialog
from pypinyin import lazy_pinyin

table ="""<table style="BORDER-COLLAPSE: collapse; text-align: center" borderColor=#000000 cellSpacing=0 cellPadding=2 width="100%" bgColor=#fffbf0 border=1>"""

def load_and_update(file: str) -> list:
    if os.path.exists(file):
        print("已发现 " + os.path.basename(file)+" ：")
    result = []
    with open(file,'r',encoding='utf-8') as _f:
        datas = _f.readlines()
        for data in datas:
            data = data.strip()
            if data not in result and len(data) > 0:
                result.append(data)
    # 排序
    #result.sort()
    # 用拼音排序
    result.sort(key=lambda name: " ".join(lazy_pinyin(name.upper())))
    print("、".join(result))
    with open(file,'w',encoding='utf-8') as _f:
        _f.writelines([line+"\n" for line in result])
    return result

def generate_output(data_list: list) -> str:
    # CHM不支持多列布局css，只能手动打个表了
    if len(data_list) < 4:
        return table+"<tr>"+"".join(["<td>"+data+"</td>" for data in data_list])+"</tr></table>"
    quarter = math.ceil(len(data_list)/4)
    split_list = [data_list[:quarter],data_list[quarter:quarter*2],data_list[quarter*2:quarter*3],data_list[quarter*3:]]
    len_list = [len(split_list[0]),len(split_list[1]),len(split_list[2]),len(split_list[3])]
    result =[]
    for index in  range(quarter):
        sub_result = []
        for sub_index in range(4):
            if index < len_list[sub_index]:
                sub_result.append("<td>"+split_list[sub_index][index]+"</td>")
        result.append("<tr>" + "".join(sub_result) + "</tr>\n")
    return table+"\n"+"\n".join(result)+"\n</table>"

if __name__ == "__main__":
    thanks_list= load_and_update()
    print("已更新翻译贡献者列表。")
    root = tk.Tk()
    root.withdraw()
    input_path = '../速查/'
    relative_input_path = os.path.relpath(input_path,"../")
    print("文件夹地址：./"+input_path)
    htm_name = os.path.basename(input_path)
    print("htm名称："+htm_name+"_生成.htm")
    object_list = []
    for folder, dirs, files in os.walk(input_path):
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
        
        with open("../"+htm_name+"_生成.htm",'wb') as _f:
            _f.write(codecs.BOM_UTF16_LE)
            _f.write((PREFIX + str(len(object_list))).encode('utf-16-le'))
            for object_str in object_str_list:
                _f.write(("\n"+object_str).encode('utf-16-le'))
        print("已完成制作！")
    else:
        print("已取消")