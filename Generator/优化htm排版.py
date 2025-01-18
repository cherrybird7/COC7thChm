import os
import re
from pathlib import Path

def convert_tags_to_lowercase(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 查找所有HTML标签
    tags = re.findall(r'<[^>]+>', content)
    
    # 检查是否有大写标签
    has_uppercase = any(tag != tag.lower() for tag in tags)
    
    if has_uppercase:
        print(f'发现大写标签，正在转换文件: {file_path}')
        
        # 将连续4个空格替换为制表符（支持全角和半角空格）
        content = re.sub(r'[ 　]{4}', '\t', content)
        
        # 合并被分成多行的HTML元素
        content = re.sub(r'>\s*[\r\n]+\s*<', '><', content)
        
        # 删除标签内容中的换行符
        content = re.sub(r'(<[^>]+>)[\r\n]+', r'\1', content)
        content = re.sub(r'[\r\n]+(<[^>]+>)', r'\1', content)
        
        # 处理<br>标签
        content = re.sub(r'([^\n])<br>', r'\1\n<br>', content)
        
        # 将所有标签转换为小写
        new_content = re.sub(r'<([^>]+)>', lambda match: f'<{match.group(1).lower()}>', content)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
    else:
        print(f'未发现大写标签: {file_path}')

def main():
    # 获取COC7thChm目录
    current_dir = Path(__file__).parent.parent
    
    # 遍历所有HTML文件
    for file_path in current_dir.rglob('*.htm*'):
        # 跳过Generator目录
        if 'Generator' in str(file_path):
            continue
        try:
            convert_tags_to_lowercase(file_path)
        except Exception as e:
            print(f'处理文件 {file_path} 时出错: {str(e)}')

if __name__ == '__main__':
    main()