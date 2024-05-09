import os
import subprocess
import csv
import re
import locale

def get_ping_average(server):
    # 移除端口（如果存在），仅保留主机部分
    if ':' in server:
        host, _ = server.rsplit(':', 1)  # 仅保留主机名，忽略端口（因为ping命令不支持端口）
        server = host

    ping_command = f"ping {server}"  # 直接使用ping命令处理IPv4和IPv6地址，依赖于系统默认行为

    try:
        ping_output = subprocess.check_output(ping_command, shell=True, stderr=subprocess.DEVNULL, universal_newlines=True)
    except subprocess.CalledProcessError:
        return None  # 如果ping失败，返回None表示无法获取平均值

    # 解析ping输出，提取平均响应时间（单位：毫秒）
    avg_ms_pattern = r"rtt min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)"
    match = re.search(avg_ms_pattern, ping_output)
    if match:
        return float(match.group(2))  # 返回平均响应时间（ms])

    return None  # 如果无法解析出平均响应时间，返回None


def ping_and_display(server):
    # 移除端口（如果存在），仅保留主机部分
    if ':' in server:
        host, _ = server.rsplit(':', 1)  # 仅保留主机名，忽略端口（因为ping命令不支持端口）
        server = host

    ping_command = f"ping {server}"  # 直接使用ping命令处理IPv4和IPv6地址，依赖于系统默认行为

    p = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            print(line.decode(locale.getpreferredencoding(False)).strip())  # 使用系统默认编码解码ping命令的输出

    # 获取退出状态码
    exit_code = p.wait()
    if exit_code == 0:
        # ping成功，尝试计算平均响应时间
        ping_avg = get_ping_average(server)
        return ping_avg if ping_avg is not None else 'N/A'
    else:
        return None  # ping失败，返回None表示无法获取平均值


# 打开输出CSV文件
with open('csv/ping.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)

    # 写入表头
    writer.writerow(['Server', 'Ping Value (ms)'])

    # 读取输入TXT文件
        with open('txt/server.txt', 'r', encoding='utf-8') as input_file:
        for line in input_file:
            server, address = line.strip().split(',')  # 分割行内容为server和address

            # 计算并显示ping情况，同时获取平均响应时间
            ping_avg = ping_and_display(server)

            # 将结果写入CSV文件
            writer.writerow([server, ping_avg])

print("Ping results written to csv/ping.csv")
