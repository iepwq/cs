import re
import requests
from collections import OrderedDict

def check_timeshift_support(m3u8_content):
    """检查M3U8内容是否支持时移，通过寻找#EXT-X-PROGRAM-DATE-TIME标签"""
    return 1 if re.search(r'#EXT-X-PROGRAM-DATE-TIME:', m3u8_content, re.IGNORECASE) else 2

def process_urls(input_file_path='txt/test_unique.txt', output_file_path='txt/review.txt'):
    """
    读取输入文件，去重后检测每行URL是否指向支持时移的HLS流。结果以 'name,url,height,elapsed_time,review' 形式写入输出文件。
    同时，检查height的值，如果值大于1080，则在name原值后面加上UHD字样，不大于1080的不处理。

    参数:
    - input_file_path: 输入文件路径，默认为 'txt/test_unique.txt'
    - output_file_path: 输出文件路径，默认为 'txt/review.txt'

    无返回值。
    """

    try:
        unique_urls = OrderedDict()

        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                line_parts = line.strip().split(',')

                if len(line_parts) < 4:
                    print(f"跳过格式不正确的行：{line}")
                    continue

                name, url, height_str, elapsed_time = line_parts[:4]

                try:
                    height = int(height_str)
                except ValueError:
                    print(f"跳过高度值无法转换为整数的行：{line}")
                    continue

                # 新增逻辑：检查height值并根据其大小在name原值后面添加UHD字样
                if height > 1080:
                    name += "UHD"

                # 下载并检查M3U8内容以判断时移支持情况
                response = requests.get(url)
                if response.status_code == 200:
                    review = check_timeshift_support(response.text)
                    # 确保每个URL对应的review值被正确记录
                    unique_urls[url] = (name, height_str, elapsed_time, review)
                else:
                    print(f"无法获取URL内容：{url}")
                    continue

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for url, (name, height_str, elapsed_time, review) in unique_urls.items():
                output_file.write(f"{name},{url},{height_str},{elapsed_time},{review}\n")

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
process_urls()
