'''
File: run.py
Project: ly-certification
Created: 2025-01-09 02:58:19
Author: Victor Cheng
Email: hi@victor42.work
Description: 
'''

import os
import pandas as pd
import shutil
from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

def get_system_paths() -> tuple[str, str]:
    """获取系统下载目录和考试记录存储目录的路径

    :return tuple[str, str]: 包含下载目录和记录目录的元组
        - downloads_dir: 系统下载文件夹路径
        - records_dir: 考试记录存储目录路径
    """
    downloads_dir = str(Path.home() / "Downloads")
    records_dir = os.path.join(os.path.dirname(__file__), 'records')
    os.makedirs(records_dir, exist_ok=True)
    return downloads_dir, records_dir

def move_exam_files(downloads_dir: str, records_dir: str) -> None:
    """移动下载文件夹中的考试文件到records目录

    :param str downloads_dir: 下载文件夹路径
    :param str records_dir: 考试记录存储目录路径
    """
    for file in os.listdir(downloads_dir):
        if file.startswith('ly_exam_') and file.endswith('.csv'):
            src = os.path.join(downloads_dir, file)
            dst = os.path.join(records_dir, file)
            shutil.move(src, dst)

def get_sorted_exam_files(records_dir: str) -> list[str]:
    """获取并按时间排序的考试文件列表

    :param str records_dir: 考试记录存储目录路径
    :return list[str]: 按创建时间排序的文件名列表
    """
    csv_files = [f for f in os.listdir(records_dir) if f.endswith('.csv')]
    return sorted(csv_files, key=lambda x: os.path.getctime(os.path.join(records_dir, x)))

def read_exam_file(file_path: str) -> pd.DataFrame:
    """读取考试文件并去重

    :param str file_path: 考试文件路径
    :return pd.DataFrame: 去重后的考试数据
    """
    df = pd.read_csv(file_path)
    return df.drop_duplicates(subset=['题干'])

def estimate_size_by_two_exams(df1, df2):
    """通过两次考试数据估算题库总量

    :param pd.DataFrame df1: 第一次考试数据
    :param pd.DataFrame df2: 第二次考试数据
    :return float | None: 估算的题库总量，如果无法估算则返回None
    """
    total1 = len(df1)
    total2 = len(df2)
    
    # 找出重复出现的题目
    repeated_questions = df2[df2['题干'].isin(df1['题干'])]
    repeated_count = len(repeated_questions)
    
    if repeated_count > 0:
        return (total1 * total2) / repeated_count
    return None

def analyze_question_bank_size(csv_files, records_dir):
    """分析题库大小，计算多次估算的统计结果

    :param list[str] csv_files: 考试文件列表
    :param str records_dir: 考试记录存储目录路径
    :return tuple[list[pd.DataFrame], float, int] | None: 包含所有考试数据列表、覆盖率和估算题库总量的元组，如果无法分析则返回None
    """
    if len(csv_files) < 2:
        return None
    
    # 读取所有文件
    file_dfs = []
    for file in csv_files:
        file_path = os.path.join(records_dir, file)
        df = read_exam_file(file_path)
        file_dfs.append(df)
    
    # 进行多次两两对比估算
    estimations = []
    for i in range(len(file_dfs)-1):
        estimate = estimate_size_by_two_exams(file_dfs[i], file_dfs[i+1])
        if estimate is not None:
            estimations.append(estimate)
    
    if not estimations:
        print("\n无法估算题库总量，所有对比都没有重复题目")
        return None
    
    # 计算统计数据
    avg_estimation = sum(estimations) / len(estimations)
    min_estimation = min(estimations)
    max_estimation = max(estimations)
    # 计算标准差
    variance = sum((x - avg_estimation) ** 2 for x in estimations) / len(estimations)
    std_deviation = variance ** 0.5
    
    # 打印估算原理和公式说明
    print("\n题库总量估算原理:")
    print("基于捕获-再捕获方法(Capture-Recapture Method)进行估算")
    print("计算公式: N = (C₁ × C₂) ÷ M")
    print("其中:")
    print("N: 题库总量")
    print("C₁: 第一次抽取的题目数量")
    print("C₂: 第二次抽取的题目数量")
    print("M: 两次抽取中重复出现的题目数量")
    
    # 打印详细的估算过程
    print("\n题库总量多次估算结果:")
    for i, est in enumerate(estimations):
        deviation = abs(est - avg_estimation) / std_deviation
        note = ""
        if deviation > 2:
            note = " (异常值)"
        print(f"第{i+1}次估算 (对比第{len(csv_files)-i-1}份和第{len(csv_files)-i}份文件): {int(est)} 道题{note}")
    
    print("\n统计结果:")
    print(f"平均值: {int(avg_estimation)} 道题")
    print(f"标准差: {int(std_deviation)} 道题")
    print(f"最小值: {int(min_estimation)} 道题")
    print(f"最大值: {int(max_estimation)} 道题")
    print(f"估算次数: {len(estimations)} 次")

    # 计算已刷题目总数和错题总数
    all_questions = set()
    incorrect_questions = set()
    for df in file_dfs:
        all_questions.update(df['题干'].tolist())
        incorrect_questions.update(df[df['结果'] == '错误']['题干'].tolist())
    total_seen = len(all_questions)
    total_incorrect = len(incorrect_questions)
    
    coverage_rate = total_seen/int(avg_estimation)
    
    print("\n结论:")
    print(f"整个题库大约有 {int(avg_estimation)} 道题")
    print(f"目前已刷到 {total_seen} 道不同的题 (覆盖率{coverage_rate*100:.1f}%)")
    print(f"其中错题集积累了 {total_incorrect} 道题 (错误率{total_incorrect/total_seen*100:.1f}%)")
    
    # 检查估算值的离散程度
    max_deviation = max(abs(x - avg_estimation) for x in estimations) / std_deviation
    if max_deviation > 2:
        print("\n注意: 部分估算值的偏差超过2个标准差，可能存在以下原因：")
        print("1. 题库在期间可能发生了变化")
        print("2. 抽题规则可能发生了变化")
        print("3. 样本量可能不够大")
        print(f"4. 最大偏差为 {max_deviation:.1f} 个标准差")

    return file_dfs, coverage_rate, int(avg_estimation)  # 返回数据框列表、覆盖率和估算总量

def format_questions_to_markdown(df: pd.DataFrame, title: str) -> str:
    """将题目数据格式化为markdown格式

    :param pd.DataFrame df: 包含题目的数据
    :param str title: 文档标题
    :return str: 格式化后的markdown文本
    """
    content = []
    content.append(f"# {title}\n")
    content.append(f"总共 {len(df)} 道题\n\n---\n")

    # 按题型分类
    question_types = df['题型'].unique()
    for qtype in sorted(question_types):
        type_questions = df[df['题型'] == qtype]
        content.append(f"\n# {qtype}\n")
        content.append(f"共 {len(type_questions)} 道题\n\n---\n")
        
        for _, row in type_questions.iterrows():
            content.append(f"## {row['题干']}\n")
            options = row['选项'].replace(' | ', '  \n')
            content.append(f"{options}\n")
            content.append(f"正确答案：{row['正确答案']}\n")
            content.append(f"题目解析：  \n{row['题目解析']}\n")
            content.append("---\n")
    
    return '\n'.join(content)

def get_all_unique_questions(file_dfs):
    """获取所有不重复的题目并格式化

    :param list[pd.DataFrame] file_dfs: 所有考试数据的列表
    :return str: 格式化后的markdown文本
    """
    # 获取所有不重复题目的完整信息
    all_df = pd.concat(file_dfs)
    unique_questions = all_df.drop_duplicates(subset=['题干'])
    return format_questions_to_markdown(unique_questions, "瓴羊模拟考题库")

def export_question_bank_pdf(content: str, downloads_dir: str) -> None:
    """导出题库到PDF文件

    :param str content: markdown格式的题库内容
    :param str downloads_dir: 下载文件夹路径
    """
    temp_markdown_path = os.path.join(downloads_dir, 'temp_question_bank.md')
    pdf_path = os.path.join(downloads_dir, '瓴羊模拟考题库.pdf')
    
    # 保存临时markdown文件
    with open(temp_markdown_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 转换为PDF
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(content))
    pdf.save(pdf_path)
    
    # 删除临时markdown文件
    os.remove(temp_markdown_path)
    
    print(f"题库已生成: {pdf_path}")

def get_incorrect_questions(csv_files, records_dir):
    """获取所有错题

    :param list[str] csv_files: 考试文件列表
    :param str records_dir: 考试记录存储目录路径
    :return pd.DataFrame | None: 包含错题的数据，如果没有错题则返回None
    """
    dfs = []
    for file in csv_files:
        file_path = os.path.join(records_dir, file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    if dfs:
        merged_df = pd.concat(dfs).drop_duplicates(subset=['题干'])
        incorrect_df = merged_df[merged_df['结果'] == '错误']
        
        # 保存到incorrect.csv
        output_path = os.path.join(os.path.dirname(__file__), 'incorrect.csv')
        incorrect_df.to_csv(output_path, index=False)
        
        return incorrect_df
    return None

def export_incorrect_pdf(content: str, downloads_dir: str) -> None:
    """导出错题集到PDF文件

    :param str content: markdown格式的错题集内容
    :param str downloads_dir: 下载文件夹路径
    """
    temp_markdown_path = os.path.join(downloads_dir, 'temp_incorrect.md')
    pdf_path = os.path.join(downloads_dir, '瓴羊模拟考错题集.pdf')
    
    # 保存临时markdown文件
    with open(temp_markdown_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 转换为PDF
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(content))
    pdf.save(pdf_path)
    
    # 删除临时markdown文件
    os.remove(temp_markdown_path)
    
    print(f"\n错题集已生成: {pdf_path}")

def main() -> None:
    """程序入口函数，处理考试文件并生成分析结果"""
    downloads_dir, records_dir = get_system_paths()
    move_exam_files(downloads_dir, records_dir)
    
    csv_files = get_sorted_exam_files(records_dir)
    if len(csv_files) >= 2:
        # 进行多次估算并计算平均值
        result = analyze_question_bank_size(csv_files, records_dir)
        
        if result:
            file_dfs, coverage_rate, total_questions = result
            
            # 只有当覆盖率达到90%时才生成题库PDF
            if coverage_rate > 0.9:
                print(f"\n题库覆盖率已达到 {coverage_rate*100:.1f}%，超过90%，开始生成题库...")
                content = get_all_unique_questions(file_dfs)
                export_question_bank_pdf(content, downloads_dir)
            
            # 处理错题并生成PDF
            incorrect_df = get_incorrect_questions(csv_files, records_dir)
            if incorrect_df is not None:
                content = format_questions_to_markdown(incorrect_df, "瓴羊模拟考错题集")
                export_incorrect_pdf(content, downloads_dir)
    
    elif len(csv_files) == 1:
        print("目前只有一次考试记录，无法估算题库总量")
        incorrect_df = get_incorrect_questions(csv_files, records_dir)
        if incorrect_df is not None:
            content = format_questions_to_markdown(incorrect_df, "瓴羊模拟考错题集")
            export_incorrect_pdf(content, downloads_dir)
    else:
        print("没有找到CSV文件")

if __name__ == "__main__":
    main()
