import os

def convert_to_utf8_bom(input_file, output_file):
    with open(input_file, 'rb') as f:
        content = f.read()
    
    with open(output_file, 'wb') as f:
        # 写入UTF-8 BOM
        f.write(b'\xef\xbb\xbf')
        # 将内容编码为UTF-8
        f.write(content.decode('utf-8').encode('utf-8'))

def convert_directory_encoding(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".md")):  # 只转换特定类型的文件
                input_file = os.path.join(root, file)
                output_file = os.path.join(root, f"utf8_bom_{file}")  # 输出文件名
                try:
                    convert_to_utf8_bom(input_file, output_file)
                    print(f"Converted: {input_file} to {output_file}")
                except Exception as e:
                    print(f"Error converting {input_file}: {e}")

# 指定要转换的目录
directory_path = './怪物之锤/第2卷 神话神祗/2.神话诸神'
convert_directory_encoding(directory_path)
