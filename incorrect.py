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
merged_df = pd.concat(dfs).drop_duplicates(subset=['题干'])

# 筛选出错误的题目
incorrect_df = merged_df[merged_df['结果'] == '错误']

# 保存到incorrect.csv
output_path = os.path.join(os.path.dirname(__file__), 'incorrect.csv')
incorrect_df.to_csv(output_path, index=False)

# 生成markdown文件
markdown_content = []
markdown_content.append(f"总共 {len(incorrect_df)} 道错题\n\n---\n")

for _, row in incorrect_df.iterrows():
    markdown_content.append(f"## \[{row['题型']}\] {row['题干']}\n")
    markdown_content.append(f"{row['选项']}\n")
    markdown_content.append(f"正确答案：{row['正确答案']}  ")
    markdown_content.append(f"我的答案：{row['我的答案']}\n")
    markdown_content.append(f"题目解析：  \n```\n{row['题目解析']}\n```\n")
    markdown_content.append("---\n")

# 保存markdown文件到指定目录
markdown_path = '/Users/colachan/odrive/OneDrive/文档/notebook/⚓ Note port/瓴羊模拟考错题集.md'
with open(markdown_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(markdown_content))
