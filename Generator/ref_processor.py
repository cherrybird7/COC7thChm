import re
import os

def process_refs(htm_path):
    # 读取htm文件
    with open(htm_path, 'r', encoding='utf-8') as f:
        htm_content = f.read()
    
    # 匹配<ref>标签
    ref_matches = re.findall(r'<ref>(.*?)</ref>', htm_content)
    
    # 生成注释编号
    ref_dict = {i+1: match for i, match in enumerate(ref_matches)}
    
    # 替换<ref>为<sup>
    for num, text in ref_dict.items():
        htm_content = htm_content.replace(
            f'<ref>{text}</ref>', 
            f'<sup>{num}</sup>'
        )
    
    # 在</body>前插入注释
    ref_notes = '<p>'
    for i, (num, text) in enumerate(ref_dict.items()):
        if i > 0:
            ref_notes += '\n<br>'
        ref_notes += f'<b>{num}:</b>{text}'
    ref_notes += '</p>'
    htm_content = htm_content.replace(
        '</body>', 
        f'{ref_notes}\n</body>'
    )
    
    # 直接覆盖原文件
    with open(htm_path, 'w', encoding='utf-8') as f:
        f.write(htm_content)
    
    return htm_path

def process_directory(root_dir):
    # 遍历目录
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.htm'):
                file_path = os.path.join(root, file)
                try:
                    process_refs(file_path)
                    print(f'处理完成：{file_path}')
                except Exception as e:
                    print(f'处理失败：{file_path}，错误：{str(e)}')

if __name__ == '__main__':
    # 处理克苏鲁神话原著目录
    root_dir = '克苏鲁神话原著'
    process_directory(root_dir)
    print('全部文件处理完成')
