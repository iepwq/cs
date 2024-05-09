import requests
from bs4 import BeautifulSoup
import re

CONSECUTIVE_EMPTY_PAGES_THRESHOLD = 10  # 定义连续空页阈值

import random
import string

def generate_random_user_agent():
    # 定义浏览器、操作系统及版本信息
    browsers = ["Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3"]

    windows_versions = ["10.0", "8.1", "7 SP1"]
    macos_versions = ["10.12.5", "10.13.Ⅹ", "10.14.Y"]  # 替换 X 和 Y 为合适的版本号
    chrome_versions = ["58.0.3029.110", "59.0.3071.115", "51.0.2704.103"]  # 添加更多...

    # 随机选择一个浏览器模板和对应的版本信息
    browser_template = random.choice(browsers)
    windows_version = random.choice(windows_versions) if "Windows" in browser_template else ""
    macos_version = random.choice(macos_versions) if "MacOS" in browser_template else ""
    chrome_version = random.choice(chrome_versions)

    # 替换模板中的占位符
    user_agent = browser_template.format(
        windows_version=windows_version,
        macos_version=macos_version,
        chrome_version=chrome_version
    )

    return user_agent

random_user_agent = generate_random_user_agent()

headers = {
    'User-Agent': random_user_agent,
}
print(random_user_agent)

#response = requests.get('http://example.com', headers=headers)


def extract_text(element):
    """
    提取指定元素的文本内容，并使用正则表达式移除所有空白字符。
    """
    try:
        text = element.text.strip()
        text = re.sub(r'[\r\n]+', '', text)  # 移除所有换行符（包括'\r'和'\n'）
        text = re.sub(r'\s+', ' ', text)  # 将其他连续空白字符替换为单个空格
        return text.strip()  # 最后再一次移除首尾空格
    except AttributeError as e:
        print(f"Error while extracting text: {e}")
        return ""

def extract_data_from_result_div(result_div):
    """
    从结果div中提取数据。
    """
    data = {}
    data['ip_port'] = extract_text(result_div.select_one('.channel b'))

    # 新增对`channel_count_label`的处理
    channel_count_span = result_div.select_one('div[style*="float: left"] > span')
    if channel_count_span:
        data['channel_count_label'] = extract_text(channel_count_span.previous_sibling)
    else:
        data['channel_count_label'] = "Channel Count Label Not Found"

    data['channel_count_value'] = extract_text(result_div.select_one('div[style*="float: left"] > span b'))
    data['new_online_label'] = extract_text(result_div.select_one('div[style*="float: right"] div'))
    data['launch_time_and_location'] = extract_text(result_div.select_one('div.result i'))
    return data


def save_results_to_txt(initial_url, output_file='txt/crawling_hoteliptv.txt'):
    with open(output_file, 'w', encoding='utf-8'):  # 在函数开始处添加此行，清空文件
        pass

    base_url, params = initial_url.split("?")
    page = 1
    consecutive_unwriteable_pages = 0  # 新增计数器，记录连续不可写入数据的页面数

    def print_consecutive_unwriteable_pages():
        print(f"连续不可写入数据的页面数: {consecutive_unwriteable_pages}")

    while True:
        # 打印当前正在执行的页码
        print(f"Processing Page {page}")

        url_with_page = f"{base_url}?{params}&page={page}&s=%E5%9B%9B%E5%B7%9D%E7%9C%81"
        try:
            # 发送GET请求并获取响应
            response = requests.get(url_with_page)

            # 检查响应状态码
            if response.status_code == 200:
                # 解析HTML内容
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding=response.encoding)

                all_results_empty = True
                with open(output_file, 'a', encoding='utf-8') as f:
                    for result_div in soup.select('div.result'):
                        data = extract_data_from_result_div(result_div)
                        if all(key in data for key in data.keys()):
                            # 新增条件判断，检查new_online_label的值
                            if data['new_online_label'] not in ("暂时失效", ""):
                                # 将当前结果的提取到的值写入文件
                                f.write(f"{data['ip_port']},{data['channel_count_label']},{data['channel_count_value']},{data['new_online_label']},{data['launch_time_and_location']}\n")
                                all_results_empty = False

                # 更新计数器（在写入数据后检查是否至少有一个可写入数据的记录）
                if all_results_empty:
                    consecutive_unwriteable_pages += 1
                    print_consecutive_unwriteable_pages()  # 输出当前连续不可写入数据的页面数
                    if consecutive_unwriteable_pages >= CONSECUTIVE_EMPTY_PAGES_THRESHOLD:  # 当连续3次页面无可写入数据时，结束递增
                        break
                else:
                    consecutive_unwriteable_pages = 0  # 遇到至少一个可写入数据的记录，重置计数器
                    print_consecutive_unwriteable_pages()  # 输出当前连续不可写入数据的页面数（此时为0，表示开始新的可写入数据序列）

            else:
                print(f"Request failed with status code: {response.status_code}")
                break  # 如果请求失败，跳出循环

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while requesting the URL: {e}")
            break  # 如果发生请求异常，跳出循环'
        page += 1  # 增加页码，准备请求下一页


# 示例：使用给定的URL
#initial_url = 'http://tonkiang.us/hoteliptv.php?page=1&pv=%E5%9B%9B%E5%B7%9D%E7%9C%81'  # 酒店源 四川
#initial_url = 'http://tonkiang.us/hoteliptv.php?page=1&s=%E5%8C%97%E4%BA%AC%E5%B8%82'  # 酒店源 四川
initial_url = 'http://tonkiang.us/hoteliptv.php?page=1&pv=%E5%9B%9B%E5%B7%9D%E7%9C%81&code=57717'  # 酒店源 四川

save_results_to_txt(initial_url)
