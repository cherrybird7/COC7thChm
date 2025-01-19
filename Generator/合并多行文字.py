import os
import re

def merge_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 合并多行文字，包括HTML内容和CSS样式
    merged = re.sub(r'(?<!\n)\n(?!\n|<style>|</style>)', ' ', content)
    # 处理<style>标签内的CSS
    merged = re.sub(r'(?<=<style>)(.*?)(?=</style>)', 
                   lambda m: re.sub(r'\s*\n\s*', ' ', m.group(0)), 
                   merged, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(merged)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.htm'):
                file_path = os.path.join(root, file)
                print(f'Processing: {file_path}')
                merge_lines_in_file(file_path)

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    process_directory(base_dir)
    print('All files processed!')
