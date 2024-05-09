import re

def extract_and_match(input_file_path='txt/review.txt', server_file_path='txt/server.txt', output_file_path='txt/address.txt'):
    try:
        # 读取 server 文件，构建 server 到 address 的映射及已存在 server 集合
        server_address_map = {}
        new_servers = set()  # 使用set来存储待追加的新服务器，确保唯一性
        with open(server_file_path, 'r', encoding='utf-8') as server_file:
            for line in server_file:
                try:
                    server, address = line.strip().split(',')
                    server_address_map[server] = address
                except ValueError:
                    print(f"跳过格式不正确的行：{line}")
        # 打开输出文件，准备写入
        with open(output_file_path, 'w', encoding='utf-8') as output_file:

            with open(input_file_path, 'r', encoding='utf-8') as input_file:
                for line in input_file:
                    line_parts = line.strip().split(',')

                    if len(line_parts) < 5:
                        print(f"跳过格式不正确的行：{line}")
                        continue

                    name, url, height, elapsed_time, review = line_parts[:5]

                    # 提取 url 中 :// 与之后第一个 / 之间的数据
                    match = re.search(r'(?:https?://)([^/]+)', url)
                    if match:
                        extracted_server = match.group(1)
                    else:
                        print(f"URL格式错误，无法提取server: {url}")
                        continue

                    address = server_address_map.get(extracted_server, 'OO')

                    # 新增逻辑：判断URL中是否包含 '/udp/' 或 '/rtp/', 标识tv字段
                    tv = "频道"
                    if "/udp/" in url or "/rtp/" in url:
                        tv = "IPTV"

                    # 输出结果，增加tv字段
                    output_file.write(f"{name},{url},{height},{elapsed_time},{review},{address},{tv}\n")

                    # 处理未找到对应地址的extracted_server
                    if address == 'OO' and extracted_server not in new_servers:
                        new_servers.add(extracted_server)

        # 追加新服务器到server.txt文件
        with open(server_file_path, 'a', encoding='utf-8') as server_file:
            for server in new_servers:
                server_file.write(f"{server},OO\n")

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
extract_and_match()
