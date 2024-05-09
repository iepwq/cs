import csv
import pandas as pd

import csv
import pandas as pd

def read_and_process_data(channel_file_path):
    try:
        # 使用pandas读取csv文件
        data = pd.read_csv(channel_file_path, delimiter=',', encoding='utf-8', names=['name', 'test', 'channel', 'url', 'height', 'elapsed_time', 'review', 'address', 'tv'])
        # 处理可能的格式错误行
        data['height'] = data['height'].apply(lambda x: int(x) if isinstance(x, str) and x.strip().isdigit() else x)
        data['elapsed_time'] = data['elapsed_time'].apply(lambda x: float(x) if isinstance(x, str) and x.strip().replace(',', '.').replace(' ', '').isdigit() else x)
        # 定义排序规则
        data['tv_sort_order'] = data['tv'].map({'频道': 0, 'IPTV': 1})
        sorted_data = data.sort_values(by=['tv_sort_order', 'tv', 'channel', 'review', 'height', 'elapsed_time'], ascending=[True, True, True, True, False, True]).drop(columns=['tv_sort_order'])
        return sorted_data.values.tolist()
    except FileNotFoundError:
        print(f"文件 '{channel_file_path}' 未找到。")
        return []
    except pd.errors.EmptyDataError:
        print(f"文件 '{channel_file_path}' 为空。")
        return []
    except Exception as e:
        print(f"读取文件时发生未知错误：{e}")
        return []

def write_sorted_data(output_file_path, sorted_data):
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            current_channel = None
            num = 1
            for row in sorted_data:
                if row[2] != current_channel:
                    current_channel = row[2]
                    num = 1
                else:
                    num += 1
                # 添加序号列
                row.append(num)
                writer.writerow(row)
    except IOError as e:
        print(f"写入文件时发生错误：{e}")
    except Exception as e:
        print(f"写入文件时发生未知错误：{e}")

def sort_and_record_num(channel_file_path='txt/channel.txt', output_file_path='txt/sort.txt'):
    # 读取并处理数据
    sorted_data = read_and_process_data(channel_file_path)
    # 写入处理后的数据
    write_sorted_data(output_file_path, sorted_data)

# 示例调用
sort_and_record_num()
