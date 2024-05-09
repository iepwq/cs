import os

"""
def append_and_clear(waiting_test_path='txt/waiting_test.txt', waiting_path='txt/waiting.txt'):
    
    将waiting_test.txt的内容追加到waiting.txt，并清空waiting_test.txt。

    参数:
    - waiting_test_path: 待追加文件路径，默认为'txt/waiting_test.txt'。
    - waiting_path: 目标文件路径，默认为'txt/waiting.txt'。

    无返回值。
    
    try:
        # 打开目标文件（waiting.txt）用于追加写入
        with open(waiting_path, 'a', encoding='utf-8') as waiting_file:
            # 打开待追加文件（waiting_test.txt）用于读取
            with open(waiting_test_path, 'r', encoding='utf-8') as waiting_test_file:
                # 将待追加文件内容逐行追加到目标文件
                for line in waiting_test_file:
                    waiting_file.write(line)

        # 清空待追加文件（waiting_test.txt）
        with open(waiting_test_path, 'w', encoding='utf-8'):
            pass

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
append_and_clear()
"""
def remove_duplicates(file_path):
    """
    读取指定文件中的内容，去除重复行，并将结果写回原文件。
    """
    temp_file_path = f"{os.path.splitext(file_path)[0]}_temp.txt"

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = set(f.readlines())  # 使用 set 去除重复行

    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)  # 将去重后的行写入临时文件

    os.replace(temp_file_path, file_path)  # 替换原文件为临时文件（原子操作，避免因意外中断导致原文件丢失）

# 分别对多个个文件去重
remove_duplicates('txt/over.txt')
remove_duplicates('txt/lose.txt')
remove_duplicates('txt/waiting.txt')
#remove_duplicates('txt/server.txt')
#remove_duplicates('txt/finished.txt')

def remove_overlapping_lines(overlap_source_path, overlap_target_path):
    """
    从`overlap_source_path`文件中移除与`overlap_target_path`文件中重复的行，
    并将结果写回`overlap_source_path`文件。
    """
    temp_file_path = f"{os.path.splitext(overlap_source_path)[0]}_temp.txt"

    with open(overlap_source_path, 'r', encoding='utf-8') as source_file:
        source_lines = set(source_file.readlines())

    with open(overlap_target_path, 'r', encoding='utf-8') as target_file:
        target_lines = set(target_file.readlines())

    non_overlapping_lines = source_lines.difference(target_lines)

    with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
        temp_file.writelines(non_overlapping_lines)

    os.replace(temp_file_path, overlap_source_path)

# 调用新函数，移除txt/over.txt中与txt/waiting.txt重复的行
remove_overlapping_lines('txt/over.txt', 'txt/waiting.txt')


