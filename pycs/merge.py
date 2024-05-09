import os
import re
import csv


print("对txt/finished.txt进行数据处理，保存为txt/finished_temp.txt")
def clean_data(row):
    # 使用正则表达式删除每个元素中的"$"及其右侧的所有内容
    cleaned_row = [re.sub(r'\$\s*.*$', '', item) for item in row]
    return cleaned_row

# 输入和输出文件路径
input_file_path = 'txt/finished.txt'
output_file_path = 'txt/finished_temp.txt'

# 打开输入文件，读取内容，并准备写入输出文件
try:
    with open(input_file_path, 'r', encoding='utf-8') as infile, \
            open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 遍历文件的每一行
        for row in reader:
            # 检查是否至少包含两个元素（假设name和url是必需的）
            if len(row) >= 2:
                # 清洗数据
                cleaned_row = clean_data(row)
                # 写入处理后的行
                writer.writerow(cleaned_row)
            else:
                # 跳过格式不合的行
                continue

    print("finished数据处理完成，已输出至", output_file_path)

except FileNotFoundError:
    print("错误：输入文件未找到，请确保文件路径正确。")
except Exception as e:
    print(f"处理过程中发生错误：{e}")

def remove_special_chars(old_name):
    """
    从名称中移除特殊字符

    :param old_name: 原始名称字符串
    :return: 移除特殊字符后的名称字符串itx
    """
    return old_name.replace(' ', '').replace('FHD', '').replace('高清', '').replace('超清', '').replace('-', '').replace('UHD', '').replace('_', '').replace('HD', '').replace('「IPV6」', '')

def check_file(file_path, url_column_index, url):
    """
    检查URL是否存在于指定文件中，增加行格式检查

    :param file_path: 文件路径
    :param url_column_index: URL所在列的索引
    :param url: 待检查的URL
    :return: 布尔值，URL如果存在于文件中则返回True，否则返回False
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > url_column_index and url == row[url_column_index]:
                return True
    return False

def clean_and_deduplicate_new_url(file_path):
    """
    ...（函数注释保持不变）...
    """
    cleaned_data = {}
    with open(file_path, 'r', encoding='utf-8') as new_file:
        for line in new_file:
            # 跳过包含#genre#或以#h开头后跟数字的行
            if '#genre#' in line or '#h' in line or not line.strip():
                continue

            # 检查分割后是否有至少两个元素
            parts = line.strip().split(',', 1)
            if len(parts) >= 2:  # 确保能正确解包
                name, raw_url = parts[0], parts[1]
                url = trim_url_after_char(raw_url)
                cleaned_key = f"{name},{url}"
                if cleaned_key not in cleaned_data:
                    cleaned_data[cleaned_key] = f"{name},{url}"
            else:
                # 可选处理：打印警告或直接跳过该行
                print(f"警告：行 '{line.strip()}' 缺少预期的逗号分隔符，已跳过。")
    return list(cleaned_data.values())


def extract_url(line, format_type):
    """
    根据文件格式提取URL，增加对格式的检查

    :param line: 文件的某一行
    :param format_type: 文件格式类型，'finished' 或 'test'
    :return: 提取的URL字符串，如果格式不匹配则返回None
    """
    if format_type == 'finished':
        # 确保行中有至少一个逗号
        parts = line.strip().split(',')
        if len(parts) > 1:
            return parts[1].split('${')[0]
    elif format_type == 'test':
        parts = line.strip().split(',')
        if len(parts) > 1:
            return parts[1]
    return None

def _is_duplicate(url, check_files, file_format='finished'):
    """
    检查URL是否在指定文件中重复，考虑文件的不同格式

    :param url: 待检查的URL
    :param check_files: 待检查的文件列表
    :param file_format: 文件格式，默认为'finished'
    :return: 布尔值，URL如果在某个文件中重复则返回True，否则返回False
    """
    url_to_check = extract_url(url, 'finished') if file_format == 'finished' else url
    for file_path in check_files:
        with open(file_path, 'r', encoding='utf-8') as check_file:
            for line in check_file:
                compare_url = extract_url(line, 'test' if 'test' in file_path else 'finished')
                if compare_url and url_to_check == compare_url:
                    return True
    return False

def load_rename_rules(rename_file_path):
    """
    加载重命名规则

    :param rename_file_path: 重命名规则文件的路径
    :return: 重命名规则字典
    """
    rename_rules = {}
    with open(rename_file_path, 'r', encoding='utf-8') as rename_file:
        for line in rename_file:
            new_name, old_names = line.strip().split(',')
            old_names_list = old_names.strip().split('|')
            for old_name in old_names_list:
                rename_rules[remove_special_chars(old_name)] = new_name.strip()
    return rename_rules

def apply_renaming(final_lines, rename_rules):
    """
    应用重命名规则到最终的条目列表上。

    :param final_lines: 最终条目列表
    :param rename_rules: 重命名规则字典
    :return: 应用重命名规则后的最终条目列表
    """
    renamed_lines = []
    for line in final_lines:
        name, url = line.strip().split(',', 1)
        # 应用重命名规则
        new_name = rename_rules.get(remove_special_chars(name), name)
        renamed_lines.append(f"{new_name},{url}\n")
    return renamed_lines

def trim_url_after_char(url, char='$'):
    """
    去除URL中指定字符及其右侧的所有数据

    :param url: 待处理的URL
    :param char: 指定的字符
    :return: 处理后的URL
    """
    index = url.find(char)
    if index != -1:
        return url[:index]
    return url

def merge_and_check_duplicates(new_urls, finished_file_path, output_file_path, check_files):
    """
    合并new_urls与finished.txt，同时与外部文件去重

    :param new_urls: 新URL列表
    :param finished_file_path: finished.txt文件路径
    :param output_file_path: 输出文件路径
    :param check_files: 待检查的外部文件列表
    :return: 合并并去重后的最终条目列表
    """
    # 读取finished.txt的内容
    with open(finished_file_path, 'r', encoding='utf-8') as finished_file:
        finished_lines = finished_file.readlines()

    # 合并并去重
    merged_lines = new_urls.copy()  # 使用列表的copy避免修改原列表
    for line in finished_lines:
        name, url = line.strip().split(',', 1)
        url = trim_url_after_char(url)
        if not _is_duplicate(url, check_files):
            merged_lines.append(f"{name},{url}\n")

    # 去除合并后的文件内容与外部文件的重复
    final_lines = [line for line in merged_lines if not any(_is_duplicate(line.split(',')[1], check_files))]

    # 写入最终结果到输出文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(final_lines)
    return final_lines

def read_filtered_lines(file_path):
    """从文件中读取所有非空行，并排除包含'#genre#'的行"""
    with open(file_path, 'r', encoding='utf-8') as file:
        # 在过滤空行的基础上，增加条件排除包含'#genre#'的行
        non_empty_lines = [line.strip() for line in file if line.strip() and '#genre#' not in line.strip()]
    return non_empty_lines

def main():
    # 定义文件路径
    new_file_path = 'txt/new_url.txt'
    finished_file_path = 'txt/finished_temp.txt'
    final_output_path = 'txt/merge.txt'
    check_files_for_new_urls = ['txt/test.txt', 'txt/waiting.txt', 'txt/over.txt', 'txt/lose.txt', 'txt/finished_temp.txt']

    # 加载重命名规则
    rename_file_path = 'txt/rename.txt'  # 确保替换为实际的重命名规则文件路径
    rename_rules = load_rename_rules(rename_file_path)

    # 一、new_url内部去重（同时去除URL中'$'及右边的数据）
    new_urls = clean_and_deduplicate_new_url(new_file_path)

    # 二、new_url与其他文件对比去重
    new_urls_deduped = [url for url in new_urls if not _is_duplicate(url, check_files_for_new_urls)]
    #将去重后的新URL列表写入临时文件
    with open('txt/merge_temp.txt', 'w', encoding='utf-8') as temp_file:
        for url in new_urls_deduped:
            temp_file.write(url + '\n')

    # 三、new_url与finished.txt合并，先处理finished.txt的格式
    finished_processed_lines = read_filtered_lines(finished_file_path)    # 之后，您可能需要重新考虑如何去重和合并，因为直接比较或合并逻辑可能需要依据新的数据格式进行调整。
    # 这里简单示意，实际情况可能需要结合前面的逻辑进行适当调整
    # 注意：此处示例逻辑简化，实际应用中需根据业务需求细化处理
    all_lines = new_urls_deduped + finished_processed_lines

    # 四、合并文件与txt/test.txt、txt/waiting.txt对比去重
    # 注意：这里假设all_lines中的数据已经是处理过的，去除了内部重复。如果有重复需要去除，应在合并到all_lines之前完成。
    additional_check_files = ['txt/test.txt',  'txt/over.txt']
    # 确保每个url都是唯一的，可以通过转换为集合再转回列表实现，但这取决于业务需求是否允许这样的去重方式
    unique_all_lines = list(set(all_lines))  # 示例去重操作，根据实际需求调整
    final_lines = [
        line for line in unique_all_lines
        if len(line.strip().split(',')) > 1 and not _is_duplicate(extract_url(line, 'finished'), additional_check_files, 'test')
    ]
    for i, line in enumerate(final_lines):
        if not line.endswith('\n'):
            final_lines[i] = line + '\n'

    # 五、在写入前应用重命名规则
    renamed_final_lines = apply_renaming(final_lines, rename_rules)

    # 写入最终去重并重命名后的合并结果
    with open(final_output_path, 'w', encoding='utf-8') as final_file:
        final_file.writelines(renamed_final_lines)


if __name__ == "__main__":
    main()


# 删除异常源
def process_merge_txt():
    with open('txt/merge.txt', 'r+', encoding='utf-8') as finished_file, \
            open('txt/discard.txt', 'r', encoding='utf-8') as discard_file:

        finished_lines = finished_file.readlines()
        discard_keywords = discard_file.read().splitlines()

        num_deleted_lines = 0
        new_finished_lines = []

        for line in finished_lines:
            line_parts = line.strip().split(',')
            name = line_parts[0]
            url = line_parts[1].split('$')[0]

            if any(keyword in url for keyword in discard_keywords):
                num_deleted_lines += 1
            else:
                new_finished_lines.append(line)

        finished_file.seek(0)
        finished_file.truncate()
        finished_file.writelines(new_finished_lines)

    print(f"删除异常源{num_deleted_lines}行。")

process_merge_txt()
