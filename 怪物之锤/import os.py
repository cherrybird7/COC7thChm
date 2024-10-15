import os

# 指定要转换的目录
directory = r'd:\COC不全书\CoC-Necronomicon\怪物之锤'

# 遍历指定目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.htm'):
        file_path = os.path.join(directory, filename)
        # 读取文件内容
        with open(file_path, 'r', encoding='gbk') as f:
            content = f.read()

        # 保存为新的编码格式
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

print("编码转换完成！")