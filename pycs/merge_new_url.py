import os
import csv

print("删除`old_name`中的空格、HD、FHD、高清、超清、-、_、UHD")
def remove_special_chars(old_name):
    """
    删除`old_name`中的空格、HD、FHD、高清、超清、-。

    参数:
    - old_name: 原始名称字符串。

    返回:
    - 处理后的名称字符串。
    """
    return old_name.replace(' ', '').replace('FHD', '').replace('高清', '').replace('超清', '').replace('-', '').replace('UHD', '').replace('_', '').replace('HD', '').replace('「IPV6」', '')

def _is_duplicate(url, finished_file_path, over_file_path, lose_file_path, waiting_file_path, test_file_path):
    def check_file(file_path, url_column_index=1):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    #candidate_url = row[url_column_index].strip().lower()
                    candidate_url = row[url_column_index].strip()
                    # 添加以下代码，移除 $ 及其右侧内容
                    dollar_index = candidate_url.find('$')
                    if dollar_index != -1:
                        candidate_url = candidate_url[:dollar_index]

                    if url == candidate_url:
                        return True
                except IndexError:
                    continue
            return False

    # 检查URL是否存在于弃用文件中
    if check_file(finished_file_path):
        return True

    # 检查URL是否存在于弃用文件中
    if check_file(over_file_path):
        return True

    # 检查URL是否存在于永久弃用文件中
    if check_file(lose_file_path):
        return True

    # 检查URL是否存在于待处理文件中
    if check_file(waiting_file_path):
        return True

    # 检查URL是否存在于测试文件中（提取第2列作为URL）
    if check_file(test_file_path, url_column_index=1):
        return True

    return False

print("查询源url是否被使用过")

print("new_url,重命名rename,并去除merge、over、lose、test、waiting、finished重复的URL")
def merge(new_file_path='txt/new_url.txt',   finished_file_path='txt/finished.txt', merge_file_path='txt/merge.txt', over_file_path='txt/over.txt',lose_file_path='txt/lose.txt', waiting_file_path='txt/waiting.txt', rename_file_path='txt/rename.txt',test_file_path='txt/test.txt'):
    """
    合并新规则文件，并去除与已完成文件重复的URL（仅在去重时将http://与https://视为相同）。如果URL在重命名文件中有映射关系，则替换URL对应的名称。

    参数:
    - new_file_path: 新规则文件的路径，默认为'txt/new_url.txt'。
    - merge_file_path: 合并后输出文件的路径，默认为'txt/merge.txt'。
    - over_file_path: 被放弃文件的路径，默认为'txt/over.txt'。
    - lose_file_path: 被永久放弃文件的路径，默认为'txt/lose.txt'。
    - waiting_file_path: 待处理文件的路径，默认为'txt/waiting.txt'。
    - rename_file_path: URL重命名规则文件的路径，默认为'txt/rename.txt'。
    - test_file_path: 测试文件路径，默认为'txt/test.txt'。

    无返回值。
    """

    try:
        # 读取规则文件和重命名规则
        with open(new_file_path, 'r', encoding='utf-8') as new_file:
            new_lines = new_file.readlines()

        # 更新：构建重命名字典，处理old_name
        with open(rename_file_path, 'r', encoding='utf-8') as rename_file:
            rename_dict = {}
            for line in rename_file:
                new_name, old_names = line.strip().split(',')
                old_names_list = old_names.strip().split('|')

                # 处理每个old_name，删除空格、HD、FHD、高清、超清、-
                processed_old_names = [remove_special_chars(old_name) for old_name in old_names_list]

                for processed_old_name in processed_old_names:
                    rename_dict[processed_old_name] = new_name.strip()

        # 使用集合存储已处理的URL（统一为https://形式），以提高查找效率
        seen_https_urls = set()

        # 合并并去重
        with open(merge_file_path, 'w', encoding='utf-8') as merge_file:
            for line in new_lines:
                line = line.strip()

                # 删除行中 $ 及其右侧数据
                dollar_index = line.find('$')
                if dollar_index != -1:
                    line = line[:dollar_index]

                # 过滤包含 #genre#、#h 的行及空白行
                if '#genre#' in line or '#h' in line or not line:
                    continue

                if ',' not in line or line.count(',') != 1:
                    continue  # 跳过格式不正确的行

                # 添加异常处理，确保分割得到至少两个元素
                try:
                    name, url = line.split(',')[:2]
                except ValueError:
                    print(f"跳过格式异常的行：{line}")
                    continue

                # 将URL转换为https://形式（若为http://），用于去重判断
                #url_for_dup_check = url.replace('http://', 'https://', 1).lower()  # 修改：统一转换为小写进行去重判断
                url_for_dup_check = url.replace('http://', 'https://', 1)  # 修改：统一不转换为小写进行去重判断
            # 检查URL是否未被处理且不存在于弃用和等待处理的文件中
                #if url_for_dup_check not in seen_https_urls and not _is_duplicate(url.lower(), finished_file_path, over_file_path, lose_file_path, waiting_file_path, test_file_path):  # 修改：传入统一转换为小写的URL
                if url_for_dup_check not in seen_https_urls and not _is_duplicate(url, finished_file_path, over_file_path, lose_file_path, waiting_file_path, test_file_path):  # 修改：传入统一不转换为小写的URL
                    # 应用remove_special_chars()函数处理name，无论是否存在重命名规则
                    processed_name = remove_special_chars(name)

                    # 如果存在重命名规则，则应用
                    if processed_name in rename_dict:
                        name = rename_dict[processed_name]
                    else:
                        name = processed_name  # 使用处理过的name

                    merge_file.write(f"{name},{url}\n")  # 保持原形态写入merge_file
                    seen_https_urls.add(url_for_dup_check)  # 将https://形式的URL加入已处理集合

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
merge()

print("删除异常源")
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