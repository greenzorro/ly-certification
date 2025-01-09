'''
File: incorrect.py
Project: ly-exam
Created: 2025-01-03 12:08:08
Author: Victor Cheng
Email: greenzorromail@gmail.com
Description: 
'''

import os
import pandas as pd
import shutil
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

# 获取系统下载文件夹路径
downloads_dir = str(Path.home() / "Downloads")

# 创建records目录(如果不存在)
records_dir = os.path.join(os.path.dirname(__file__), 'records')
os.makedirs(records_dir, exist_ok=True)

# 移动下载文件夹中的ly_exam_*.csv文件到records目录
for file in os.listdir(downloads_dir):
    if file.startswith('ly_exam_') and file.endswith('.csv'):
        src = os.path.join(downloads_dir, file)
        dst = os.path.join(records_dir, file)
        shutil.move(src, dst)

# 获取records目录下所有csv文件
csv_files = [f for f in os.listdir(records_dir) if f.endswith('.csv')]

# 读取所有csv文件并合并
dfs = []
for file in csv_files:
    file_path = os.path.join(records_dir, file)
    df = pd.read_csv(file_path)
    dfs.append(df)

# 根据题干列合并
if dfs:
    merged_df = pd.concat(dfs).drop_duplicates(subset=['题干'])
    
    # 筛选出错误的题目
    incorrect_df = merged_df[merged_df['结果'] == '错误']

    # 保存到incorrect.csv
    output_path = os.path.join(os.path.dirname(__file__), 'incorrect.csv')
    incorrect_df.to_csv(output_path, index=False)

    # 生成markdown内容
    markdown_content = []
    markdown_content.append("# 瓴羊模拟考错题集\n")  # 添加一级标题
    markdown_content.append(f"总共 {len(incorrect_df)} 道错题\n\n---\n")

    for _, row in incorrect_df.iterrows():
        markdown_content.append(f"## \[{row['题型']}\] {row['题干']}\n")  # 这些作为二级标题
        options = row['选项'].replace(' | ', '  \n')
        markdown_content.append(f"{options}\n")
        markdown_content.append(f"正确答案：{row['正确答案']}\n")
        markdown_content.append(f"题目解析：  \n{row['题目解析']}\n")
        markdown_content.append("---\n")

    # 保存临时markdown文件到下载目录
    temp_markdown_path = os.path.join(downloads_dir, 'temp_incorrect.md')
    pdf_path = os.path.join(downloads_dir, '瓴羊模拟考错题集.pdf')
    
    # 保存临时markdown文件
    with open(temp_markdown_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    # 转换为PDF
    pdf = MarkdownPdf(toc_level=2)  # 创建PDF对象，设置目录级别为2
    pdf.add_section(Section('\n'.join(markdown_content)))  # 添加内容
    pdf.save(pdf_path)  # 保存PDF
    
    # 删除临时markdown文件
    os.remove(temp_markdown_path)

else:
    print("没有找到需要处理的CSV文件")
