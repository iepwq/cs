"""针对 tonkiang.us 资源搜索的一个爬虫代码"""
import requests
from bs4 import BeautifulSoup
import csv
import random
import os
from typing import List, Tuple, Set

# 定义基础URL为常量
#BASE_URL = 'http://tonkiang.us/?page=1&sn='
#BASE_URL = 'http://tonkiang.us/?page=1&tx='
BASE_URL = 'http://tonkiang.us/?page=1&ch='


def generate_random_user_agent():
    # 定义浏览器、操作系统及版本信息
    browsers = ["Mozilla/5.0 (Windows NT {windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X {macos_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.3"]

    windows_versions = ["10.0", "8.1", "7 SP1"]
    macos_versions = ["10.12.5", "10.13.X", "10.14.Y"]  # 替换 X 和 Y 为合适的版本号，使用.X和.Y作为通配符表示任意版本
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

def load_channel_names(filename='txt/ch_crawling.txt'):
    """
    从指定文件中加载频道名称列表。
    """
    channel_names = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            channel_name = line.strip()  # 移除行尾的换行符
            channel_names.append(channel_name)
    return channel_names

def fetch_programs(channel_names: List[str]) -> Tuple[List[str], List[str]]:
    name_list = []  # 存储节目名称的空列表
    url_list = []  # 存储节目URL的空列表
    name_count = 0  # 记录每轮提取到的节目名称数量
    url_count = 0   # 记录每轮提取到的节目URL数量

    total_projects = len(channel_names)  # 计算总项目数
    completed_projects = 0  # 初始化已完成项目数

    # 遍历输入的频道名称列表
    for channel_name in channel_names:
        page_url = f'{BASE_URL}{channel_name}'

        print(f"正在抓取频道: {channel_name}")
        try:
            # 生成随机User-Agent
            user_agent = generate_random_user_agent()

            # 发送GET请求，设置超时时间为10秒，同时设置自定义User-Agent
            response = requests.get(page_url, timeout=10, headers={'User-Agent': user_agent})

            # 使用BeautifulSoup解析请求返回的HTML内容
            page_soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            # 若请求过程中出现异常，打印错误信息并跳过当前频道
            print(f"Error fetching data from {page_url}: {e}")
            continue
        except Exception as e:
            # 添加对其他异常的处理，如解析错误
            print(f"Error processing page for {page_url}: {e}")
            continue

        # 使用原代码逻辑（示例保留，实际应用中需根据实际HTML结构调整）
        # 此处为示例，实际应用应根据具体需要调整解析逻辑
        tags = page_soup.find_all(style='float: left;')

        # 遍历找到的元素，提取并添加节目名称到name_list
        for tag in tags:
            name_list.append(tag.text.strip())
            name_count += 1

        tables = page_soup.find_all('table')

        for table in tables:
            tba_tags = table.find_all('tba')
            if len(tba_tags) >= 2:
                url_list.append(tba_tags[1].text.strip())
                url_count += 1

        print(f"频道 {channel_name} 抓取完成: {name_count} 个频道号, {url_count} 个直播源.")
        name_count = 0
        url_count = 0

        # 更新已完成项目数
        completed_projects += 1

        # 输出完成率与剩余项目量信息
        completion_rate = (completed_projects / total_projects) * 100
        remaining_projects = total_projects - completed_projects
        print(f"已完成 {completed_projects}/{total_projects} 个项目（{completion_rate:.2f}%），剩余 {remaining_projects} 个项目。")

    # 返回收集到的节目名称列表和URL列表
    return name_list, url_list


def save_to_file(name_list: List[str], url_list: List[str], filename='txt/crawling_iptv.txt'):
    # 检查节目名称列表和URL列表长度是否一致，若不一致则打印警告信息
    if len(name_list) != len(url_list):
        print("Warning: Name list and URL list are of different lengths. Some data may be lost.")

    # 使用set数据结构去除url_list中的重复值
    unique_url_set = set(url_list)

    # 检查去除重复值后的URL数量是否发生变化，若发生改变则打印信息
    if len(unique_url_set) < len(url_list):
        print(f"Removed {len(url_list) - len(unique_url_set)} duplicate URLs.")

    # 使用with语句以确保文件正确关闭
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # 创建CSV writer对象，用于写入数据
            writer = csv.writer(file)

            # 使用zip函数将节目名称列表和去重后的URL列表按行打包，然后通过writer.writerows()一次性写入文件
            writer.writerows(zip(name_list, list(unique_url_set)))
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

if __name__ == "__main__":
    # 加载频道名称列表
    channel_names = load_channel_names()

    # 调用fetch_programs函数，获取节目名称列表和URL列表
    name_list, url_list = fetch_programs(channel_names)

    # 调用save_to_file函数，将节目数据保存到文件
    save_to_file(name_list, url_list)
