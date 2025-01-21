def text_to_html_table(text, table_type="normal", equal_cells=False, center_text=False, has_title=False, has_header=False, first_col_width=None):
    # 将输入文本按行分割
    lines = text.strip().split('\n')
    
    # 开始构建HTML表格
    if table_type == "monster":
        html = '<table id="monstertable-table">\n'
    else:
        # 确定普通表格样式
        if equal_cells and center_text:
            table_id = "zebra-table"
        elif center_text:
            table_id = "nofixed-table"
        elif equal_cells:
            table_id = "zebrafixed-table"
        else:
            table_id = "left-table"
        html = f'<table id="{table_id}">\n'
    
    # 如果有标题行，添加标题行
    if has_title and lines:
        # 计算最大列数
        max_cols = max(len(line.split()) for line in lines)
        html += '<tr>\n'
        html += f'<th class="tabletitle" colspan="{max_cols}">{lines[0]}</th>\n'
        html += '</tr>\n'
        lines = lines[1:]  # 移除标题行
    
    # 如果有表头，添加表头行（使用<th>标签）
    if has_header and lines:
        html += '<tr>\n'
        for cell in lines[0].split():
            html += f'<th>{cell}</th>\n'
        html += '</tr>\n'
        lines = lines[1:]  # 移除表头行
    
    # 普通表格时才初始化行计数器
    if table_type != "monster":
        if not hasattr(text_to_html_table, 'row_count'):
            text_to_html_table.row_count = 0

    for line in lines:
        # 将每行按空格或制表符分割成单元格
        cells = [cell for cell in line.split() if cell]
        
        if table_type == "monster":
            # 怪物属性表使用简单格式
            html += '<tr>\n'
            for cell in cells:
                html += f'<td>{cell}</td>\n'
            html += '</tr>\n'
        elif table_type == "dice":
            # 骰点表特殊格式
            if text_to_html_table.row_count % 2 == 1:
                html += '<tr class="odd">\n'
            else:
                html += '<tr>\n'
            if cells:
                # 第一个单元格作为表头
                if table_type == "dice" and first_col_width is not None:
                    html += f'<th width="{first_col_width}%">{cells[0]}</th>\n'
                else:
                    html += f'<th>{cells[0]}</th>\n'
                # 剩余单元格作为普通单元格
                for cell in cells[1:]:
                    if not center_text:
                        html += f'<td>&nbsp;{cell}</td>\n'
                    else:
                        html += f'<td>{cell}</td>\n'
            html += '</tr>\n'
            text_to_html_table.row_count += 1
        else:
            # 普通表格
            if text_to_html_table.row_count % 2 == 1:
                html += '<tr class="odd">\n'
            else:
                html += '<tr>\n'
            for cell in cells:
                if not center_text:
                    html += f'<td>&nbsp;{cell}</td>\n'
                else:
                    html += f'<td>{cell}</td>\n'
            html += '</tr>\n'
            text_to_html_table.row_count += 1
    
    html += '</table>'
    return html

def get_yes_no(prompt):
    while True:
        answer = input(prompt + " (Y/N): ").strip().upper()
        if answer in ['Y', 'N']:
            return answer == 'Y'
        print("请输入 Y 或 N")

def get_table_type():
    while True:
        print("请选择表格类型：")
        print("1. 普通表格")
        print("2. 怪物属性表")
        print("3. 骰点表")
        choice = input("请输入数字选择 (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return ["normal", "monster", "dice"][int(choice)-1]
        print("请输入有效的数字 (1-3)")

def get_first_column_width():
    while True:
        try:
            width = int(input("请输入第一列占表格的百分比（1-100）："))
            if 1 <= width <= 100:
                return f"{width}"
            print("请输入1到100之间的整数")
        except ValueError:
            print("请输入有效的整数")

if __name__ == "__main__":
    table_type = get_table_type()
    print("\n表格样式设置：")
    first_col_width = None  # 初始化变量
    if table_type != "monster":
        equal_cells = get_yes_no("单元格是否要平分？")
        center_text = get_yes_no("文字是否要居中？")
        has_title = get_yes_no("是否有标题行？")
        has_header = get_yes_no("是否有表头？")
        if table_type == "dice":
            first_col_width = get_first_column_width()
    else:
        equal_cells = False
        center_text = False
        has_title = False
        has_header = False
    
    print("\n请输入表格内容（输入空行结束）：")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    input_text = "\n".join(lines)
    try:
        # 生成HTML文档
        html_text = (r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>表格</title>
<meta name="GENERATOR" content="WinCHM">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="d:\coc不全书\coc7thchm\style.css">
<style></style>
</head>
<body>
""")
        # 添加表格内容
        html_text += text_to_html_table(input_text, table_type, equal_cells, center_text, has_title, has_header, first_col_width)
        # 添加HTML结尾
        html_text += "\n</body>\n</html>"
        output_path = "../generated_table.htm"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_text)
        print(f"表格已保存为 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        input("\n按回车键退出...")
