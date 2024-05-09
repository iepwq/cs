import shutil
import tempfile
import os

def merge_and_clean_files(input_file="txt/channel.txt",
                          finished_file="txt/channel_finished.txt",
                          temp_dir="temp"):
    try:
        # 先将finished_file的内容追加到input_file
        append_file(input_file, finished_file)

        # 再对input_file进行去重和删除空白行
        deduplicate_and_remove_empty_lines(input_file, temp_dir)

        print(f"文件{finished_file} 的内容已追加合并到 {input_file} 中，重复项已移除，空白行已删除。")
    except Exception as e:
        print(f"处理文件时发生错误：{str(e)}")

def append_file(input_file, finished_file):
    with open(input_file, "a", encoding="utf-8") as input_file_obj:
        with open(finished_file, "r", encoding="utf-8") as finished_file_obj:
            for line in finished_file_obj:
                input_file_obj.write(line)

def deduplicate_and_remove_empty_lines(input_file, temp_dir):
    # 创建临时目录（如果不存在）
    os.makedirs(temp_dir, exist_ok=True)

    # 用去重后的临时文件替换原文件
    temp_file = os.path.join(temp_dir, "unique_lines.txt")
    backup_file = f"{input_file}.bak"

    # 备份原文件
    shutil.copy2(input_file, backup_file)

    # 读取、去重、删除空白行，并写入临时文件
    unique_lines = set()
    with open(input_file, "r", encoding="utf-8") as input_file_obj:
        with open(temp_file, "w", encoding="utf-8") as output:
            for line in input_file_obj:
                line = line.strip()

                if line and line not in unique_lines:
                    unique_lines.add(line)
                    output.write(line + "\n")

    # 替换原文件
    shutil.move(temp_file, input_file)

if __name__ == "__main__":
    merge_and_clean_files()
