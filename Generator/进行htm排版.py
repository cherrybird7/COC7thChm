import os
import re

# 需要处理的HTML标签列表
TAGS = [
    r'<html>', r'<head>', r'<title>', r'<meta', r'<link', r'<style>',
    r'</head>', r'<body>', r'<h1>', r'<h2>', r'<h3>', r'<h4>', r'<br>', r'<hr>', 
    r'<p', r'<div', r'<table', r'<tr', r'<td', r'<ul>', r'<ol>', r'<li>',
    r'</body>', r'</html>'
]

def process_file(file_path):
    """处理单个htm文件"""
    # 读取文件内容并处理BOM字符
    with open(file_path, 'rb') as f:
        raw_content = f.read()
        content = raw_content.decode('utf-8-sig')
    
    # 在每个标签前添加换行符
    for tag in TAGS:
        # 匹配标签前没有换行符的情况，包括可能存在的空格
        pattern = re.compile(f'(?<!\\n)(\\s*)({tag}[^>]*>)', re.IGNORECASE)
        content = pattern.sub(f'\n\\1\\2', content)
    
    # 写回文件并保持原有换行符格式
    with open(file_path, 'wb') as f:
        f.write(content.encode('utf-8'))

def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 遍历所有htm文件
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.htm'):
                file_path = os.path.join(root, file)
                print(f'Processing: {file_path}')
                process_file(file_path)
                
    print('All files processed!')

if __name__ == '__main__':
    main()