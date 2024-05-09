import os




def remove_special_chars(old_name):
    """
    删除`old_name`中的空格、HD、FHD、高清、超清、-。

    参数:
    - old_name: 原始名称字符串。

    返回:
    - 处理后的名称字符串。
    """
    return old_name.replace(' ', '').replace('HD', '').replace('FHD', '').replace('高清', '').replace('超清', '').replace('-', '')

def _is_duplicate(url, over_file_path, lose_file_path, waiting_file_path):
    """
    检查给定的URL是否存在于指定的弃用或等待处理文件中。

    参数:
    - url: 待检查的URL。
    - over_file_path: 被放弃文件的路径。
    - lose_file_path: 被永久放弃文件的路径。
    - waiting_file_path: 待处理文件的路径。

    返回:
    - 如果URL存在于弃用或等待处理文件中，则返回True；否则返回False。
    """
    def check_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    _, candidate_url = line.strip().split(',')[:2]
                except ValueError:
                    continue
                if url == candidate_url.strip().lower():  # 修改：比较时忽略大小写
                    return True
        return False

    # 检查URL是否存在于弃用文件中
    if check_file(over_file_path):
        return True

    # 检查URL是否存在于永久弃用文件中
    if check_file(lose_file_path):
        return True

    # 检查URL是否存在于待处理文件中
    if check_file(waiting_file_path):
        return True

    return False

def merge(new_file_path='txt/new_url.txt', finished_file_path='txt/finished.txt', merge_file_path='txt/merge.txt', over_file_path='txt/over.txt',lose_file_path='txt/lose.txt', waiting_file_path='txt/lose.txt', rename_file_path='txt/rename.txt'):
    """
    合并新规则文件和已完成文件，并去除重复的URL（仅在去重时将http://与https://视为相同）。如果URL在重命名文件中有映射关系，则替换URL对应的名称。

    参数:
    - new_file_path: 新规则文件的路径，默认为'txt/new_url.txt'。
    - finished_file_path: 已完成文件的路径，默认为'txt/finished.txt'。
    - merge_file_path: 合并后输出文件的路径，默认为'txt/merge.txt'。
    - over_file_path: 被放弃文件的路径，默认为'txt/over.txt'。
    - lose_file_path: 被永久放弃文件的路径，默认为'txt/lose.txt'。
    - waiting_file_path: 待处理文件的路径，默认为'txt/waiting.txt'。
    - rename_file_path: URL重命名规则文件的路径，默认为'txt/rename.txt'。

    无返回值。
    """

    try:
        # 读取规则文件和重命名规则
        with open(new_file_path, 'r', encoding='utf-8') as new_file:
            new_lines = new_file.readlines()
        with open(finished_file_path, 'r', encoding='utf-8') as finished_file:
            finished_lines = finished_file.readlines()

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
            for line in new_lines + finished_lines:
                line = line.strip()

                # 删除行中 $ 及其右侧数据
                dollar_index = line.find('$')
                if dollar_index != -1:
                    line = line[:dollar_index]

                # 过滤包含 #genre# 的行和空白行
                if '#genre#' in line or not line:
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
                url_for_dup_check = url.replace('http://', 'https://', 1).lower()  # 修改：统一转换为小写进行去重判断

                # 检查URL是否未被处理且不存在于弃用和等待处理的文件中
                if url_for_dup_check not in seen_https_urls and not _is_duplicate(url.lower(), over_file_path, lose_file_path, waiting_file_path):  # 修改：传入统一转换为小写的URL
                    # 如果存在重命名规则，则应用
                    processed_name = remove_special_chars(name)  # 处理name，与rename_dict中的键进行匹配
                    if processed_name in rename_dict:
                        name = rename_dict[processed_name]

                    merge_file.write(f"{name},{url}\n")  # 保持原形态写入merge_file
                    seen_https_urls.add(url_for_dup_check)  # 将https://形式的URL加入已处理集合

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")



# 示例调用
merge()


