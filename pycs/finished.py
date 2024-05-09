import re
import csv
def process_sort_txt(input_file='txt/sort.txt', output_file='txt/finished.txt'):
    # 读取并按行分割txt/sort.txt文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    prev_ch = None

    error_count = 0  # 记录遇到的索引越界错误数量

    for line_number, line in enumerate(lines, start=1):  # 使用enumerate获取行号
        try:
            # 分割当前行数据
            row = line.strip().split(',')

            # 插入行：对于具有相同第2列（即`ch`）值的连续行，在第一个不同值出现的位置前插入一行
            ch = row[1]
            tv = row[8]
            if (prev_ch is None or prev_ch != ch):
                processed_lines.append(f'{ch}{tv},#genre#\n')
            prev_ch = ch

            # 重排并格式化行
            processed_line = row[0] + ',' + row[3] + '$' + row[9] + row[7] + row[4] + '\n'  # 保留第1列，第4列，拼接第10列、第8列和第5列

            processed_lines.append(processed_line)
        except IndexError:
            error_count += 1
            print(f"第{line_number}行：发生IndexError，跳过此行。")

    print(f"共跳过{error_count}行，原因：IndexError。")
    # 输出结果：将处理后的数据写入txt/finished.txt文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

# 示例调用
process_sort_txt()
"""
#查询关键字，删除重复的行
def process_finished_txt():
    with open('txt/finished.txt', 'r+', encoding='utf-8') as finished_file, \
         open('txt/discard.txt', 'r', encoding='utf-8') as discard_file, \
         open('txt/lose.txt', 'a', encoding='utf-8') as lose_file:

        finished_lines = finished_file.readlines()
        discard_keywords = discard_file.read().splitlines()

        new_finished_lines = []
        num_deleted_lines = 0

        for line in finished_lines:
            line_parts = line.strip().split(',')
            name = line_parts[0]
            url = line_parts[1].split('$')[0]  # 仅保留$左侧的url部分

            if any(keyword in url for keyword in discard_keywords):
                lose_file.write(f"{name},{url}\n")
                num_deleted_lines += 1
            else:
                new_finished_lines.append(line)

        finished_file.seek(0)  # 移动文件指针到开头
        finished_file.truncate()  # 清空文件内容
        finished_file.writelines(new_finished_lines)

    print(f"共删除{num_deleted_lines}行，相关内容已追加到txt/lose.txt文件中。")
"""




with open('txt/test.txt', 'w', encoding='utf-8') as file:
       file.write('')
print('txt/test.txt文件已清空')



print('文件备份')

import os
import shutil
from datetime import datetime

# 定义所有需要备份的源文件路径
src_files_to_backup = [
    ("txt/finished.txt", "finished"),
    ("txt/waiting.txt", "waiting"),
    ("txt/over.txt", "over")
]

# 备份目标目录
backup_dir = "txt/backups"

# 遍历需要备份的文件
for src_file_path, base_name in src_files_to_backup:
    # 获取当前日期与时间，格式化为"YYYY-MM-DD_HH-MM-SS"
    current_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 构建备份文件名
    backup_file_name = f"{base_name}_{current_time_str}.txt"

    # 完整备份文件路径
    backup_file_path = os.path.join(backup_dir, backup_file_name)

    # 确保备份目录存在，如果不存在则创建
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # 执行文件复制操作
    shutil.copy2(src_file_path, backup_file_path)

    print(f"已成功将 '{src_file_path}' 备份至 '{backup_file_path}'。")







