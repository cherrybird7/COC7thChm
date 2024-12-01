import re
import os

# 输入的文件路径
print("请右键贴上你的文件路径（按回车结束输入）：")
file_path = input()  # 读取用户输入的文件路径
# 识别标题作为文件名
def extract_text_between(content, start_str, end_str): # 如果文件名要做进一步更改，请修改这里
            
    # 构建正则表达式
    pattern = rf'{re.escape(start_str)}(.*?){re.escape(end_str)}'
    
    # 找出所有匹配的内容
    matches = re.findall(pattern, content, re.DOTALL)
    
    return matches
# 识别分割正文内容
def slice_text_by_start_str(file_path, start_str): 
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 根据标题开始字符串切割文件内容
    parts = content.split(start_str)
    
    return parts

# 用于识别标题
start_str = '<P><STRONG><FONT color=#800000 size=5>'  # 用于识别标题的开始字符串
end_str = '</FONT></STRONG></P>'    # 用于识别标题的结束字符串
# 备用：text_string = '<P><STRONG><FONT color=#800000 size=5>'

# 切割文件
results = slice_text_by_start_str(file_path, start_str)

# 输出结果
for i, result in enumerate(results):
    if result.strip():  # 只打印非空内容
        sect = start_str + result # 原标题格式带正文，用于输出到HTML文件中
        title = extract_text_between(sect, start_str, end_str) # 纯文本标题，用于输出文件名
        # HTML前缀
        html_prefix1 = (r"""<!-- coding: gbk --><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>""")
        html_prefix2 = (f"{title[0]}")
        html_prefix3 = (r"""</title>
<meta name="GENERATOR" content="WinCHM">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<style>
html,body { 
	font-family: Arial, Helvetica, sans-serif;
}
</style>

</head>

<body>""") 
        html_suffix = (f"""\n{start_str + result}</body>
</html>""")# 插入正文
    
    # 组合完整的HTML内容
        complete_html = html_prefix1 + html_prefix2 + html_prefix3 + html_suffix
    
    # 创建新目录用于输出文件
        output_dir = 'output_files'

        if not os.path.exists(output_dir): 
            os.makedirs(output_dir)
    # 输出文件名
        filename = os.path.join(output_dir,f"{title[0]}.htm") # 文件名
        # 以上文件名为纯文本标题，输出的结果为乱序，如果需要按照条目顺序输出，请用下方代码代替上方代码
        # filename = os.path.join(output_dir,f"{i}.{title[0]}.htm")
        Defaultname =  os.path.join(output_dir,f"{i}.Default.htm") # 默认文件名,用于文件名错误时
        
    # 批量生成HTML文件
        try:
            with open(filename, 'w', encoding='utf_8') as file:
               file.write(f'{complete_html}')
               print(f"文件 {filename} 已创建。")
        except Exception as e:#如果文件名发生错误，则输出到默认文件名
            with open(Defaultname, 'w', encoding='utf_8') as file:
               file.write(f'{complete_html}')
               print(f"文件 {Defaultname} 已创建。")

print("HTML 文件已创建。")

