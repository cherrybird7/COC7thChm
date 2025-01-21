import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class TableGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("表格生成器")
        self.root.geometry("600x400")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="NSEW")
        
        # 使用说明
        ttk.Label(self.main_frame, 
                 text=f"""使用方法：在表格内容内输入表格文本，每行文本都会按顺序转换成对应单元行，一行中文字会根据空格或制表符，分成不同的单元格。
切记转换前要检查转换的文本是否有多余的空格，如汉字与英文的空格，转换前记得删掉，输出表格后在表格内加上，否则输出会出错。
选择表格类型和样式后点击生成 htm 文件。之后在wcp文件中添加新主题，勾选链接到现有的 HTML 文件，就可打开输出的表格，复制表格后再贴进相应的位置。""",
                 wraplength=500).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 表格类型选择
        self.table_type_var = tk.StringVar(value="普通表格")
        ttk.Label(self.main_frame, text="表格类型:").grid(row=1, column=0, sticky="W")
        self.table_type_combobox = ttk.Combobox(self.main_frame, textvariable=self.table_type_var,
                                              values=["普通表格", "怪物属性表", "骰点表/特征表"])
        self.table_type_combobox.grid(row=1, column=1, sticky="EW")
        self.table_type_combobox.bind("<<ComboboxSelected>>", self.update_options)
        
        # 样式选项
        self.options_frame = ttk.LabelFrame(self.main_frame, text="表格样式选项")
        self.options_frame.grid(row=2, column=0, columnspan=2, sticky="EW", pady=10)
        
        # 单元格平分
        self.equal_cells_var = tk.BooleanVar()
        self.equal_cells_check = ttk.Checkbutton(self.options_frame, text="单元格平分",
                                                variable=self.equal_cells_var)
        self.equal_cells_check.grid(row=0, column=0, sticky="W")
        
        # 文字居中
        self.center_text_var = tk.BooleanVar()
        self.center_text_check = ttk.Checkbutton(self.options_frame, text="文字居中",
                                               variable=self.center_text_var)
        self.center_text_check.grid(row=0, column=1, sticky="W")
        
        # 标题行
        self.has_title_var = tk.BooleanVar()
        self.has_title_check = ttk.Checkbutton(self.options_frame, text="包含标题行（默认第一行文字为标题行，默认单占整行）",
                                             variable=self.has_title_var)
        self.has_title_check.grid(row=1, column=0, sticky="W")
        
        # 表头
        self.has_header_var = tk.BooleanVar()
        self.has_header_check = ttk.Checkbutton(self.options_frame, text="包含表头（如有标题行，第二行文字为表头，否则第一行为表头）",
                                              variable=self.has_header_var)
        self.has_header_check.grid(row=1, column=1, sticky="W")
        
        # 第一列宽度（仅骰点表）
        self.first_col_width_label = ttk.Label(self.options_frame, text="第一列宽度(%):")
        self.first_col_width_entry = ttk.Entry(self.options_frame, width=5)
        self.first_col_width_entry.insert(0, "3")  # 设置默认值为3%
        
        # 表格内容输入
        ttk.Label(self.main_frame, text="表格内容:").grid(row=3, column=0, sticky="NW")
        self.content_text = tk.Text(self.main_frame, height=10, width=50)
        self.content_text.grid(row=4, column=0, columnspan=2, sticky="EW")
        
        # 按钮
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.generate_button = ttk.Button(self.button_frame, text="生成表格", command=self.generate_table)
        self.generate_button.grid(row=0, column=0, padx=5)
        
        self.clear_button = ttk.Button(self.button_frame, text="清空内容", command=self.clear_content)
        self.clear_button.grid(row=0, column=1, padx=5)
        
        # 配置网格布局
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(4, weight=1)
        
        # 初始化选项
        self.update_options()
    
    def update_options(self, event=None):
        table_type = self.table_type_var.get()
        if table_type == "骰点表/特征表":
            self.first_col_width_label.grid(row=2, column=0, sticky="W")
            self.first_col_width_entry.grid(row=2, column=1, sticky="W")
        else:
            self.first_col_width_label.grid_forget()
            self.first_col_width_entry.grid_forget()
    
    def generate_table(self):
        try:
            # 获取输入内容
            input_text = self.content_text.get("1.0", "end").strip()
            if not input_text:
                messagebox.showwarning("警告", "请输入表格内容")
                return
            
            # 获取表格类型
            table_type_map = {"普通表格": "normal", "怪物属性表": "monster", "骰点表/特征表": "dice"}
            table_type = table_type_map[self.table_type_var.get()]
            
            # 获取样式选项
            equal_cells = self.equal_cells_var.get()
            center_text = self.center_text_var.get()
            has_title = self.has_title_var.get()
            has_header = self.has_header_var.get()
            first_col_width = self.first_col_width_entry.get() or "3" if table_type == "dice" else "30"
            
            # 生成HTML
            html_text = self.text_to_html_table(input_text, table_type, equal_cells, center_text, has_title, has_header, first_col_width)
            
            # 生成默认文件名
            from datetime import datetime
            default_filename = f"表格_{datetime.now().strftime('%Y%m%d_%H%M%S')}.htm"
            
            # 保存文件
            file_path = filedialog.asksaveasfilename(
                defaultextension=".htm",
                filetypes=[("HTML文件", "*.htm"), ("所有文件", "*.*")],
                initialdir=os.path.dirname(os.path.abspath(__file__)),
                initialfile=default_filename
            )
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_text)
                messagebox.showinfo("成功", f"表格已保存为 {file_path}")
        
        except Exception as e:
            messagebox.showerror("错误", f"生成表格时出错: {str(e)}")
    
    def clear_content(self):
        self.content_text.delete("1.0", "end")
    
    def text_to_html_table(self, text, table_type="normal", equal_cells=False, center_text=False, has_title=False, has_header=False, first_col_width=None):
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
        
        # 初始化行计数器
        if not hasattr(self, 'row_count'):
            self.row_count = 0

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
                if self.row_count % 2 == 1:
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
                self.row_count += 1
            else:
                # 普通表格
                if self.row_count % 2 == 1:
                    html += '<tr class="odd">\n'
                else:
                    html += '<tr>\n'
                for cell in cells:
                    if not center_text:
                        html += f'<td>&nbsp;{cell}</td>\n'
                    else:
                        html += f'<td>{cell}</td>\n'
                html += '</tr>\n'
                self.row_count += 1
        
        html += '</table>'
        
        # 添加HTML文档结构
        full_html = f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>表格</title>
<meta name="GENERATOR" content="WinCHM">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="d:\\coc不全书\\coc7thchm\\style.css">
<style></style>
</head>
<body>
{html}
</body>
</html>"""
        
        return full_html

if __name__ == "__main__":
    root = tk.Tk()
    app = TableGeneratorApp(root)
    root.mainloop()
