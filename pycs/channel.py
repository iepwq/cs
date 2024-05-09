def process_chanel_and_waiting(address_file_path='txt/address.txt', ch_file_path='txt/ch.txt', channel_file_path='txt/channel.txt', waiting_file_path='txt/waiting.txt'):
    try:
        # 读取address.txt文件，存储为[(name, url, height, elapsed_time, review, address, tv)]列表
        with open(address_file_path, 'r', encoding='utf-8') as address_file:
            address_data = []
            for line in address_file:
                parts = line.strip().split(',')
                if len(parts) >= 7:
                    name, url, height, elapsed_time, review, address, tv = parts[:7]
                    address_data.append((name, url, height, elapsed_time, review, address, tv))

        # 读取ch.txt文件，构建name到(ch, channel)的映射
        ch_channel_map = {}
        with open(ch_file_path, 'r', encoding='utf-8') as ch_file:
            for line in ch_file:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    name, ch, channel = parts
                    ch_channel_map[name] = (ch, channel)

        # 分别处理address_data中的每一项，根据name是否存在于ch_channel_map，分别写入channel.txt和waiting.txt
        with open(channel_file_path, 'w', encoding='utf-8') as channel_file, open(waiting_file_path, 'a', encoding='utf-8') as waiting_file:
            for item in address_data:
                name, url, height, elapsed_time, review, address, tv = item

                if name in ch_channel_map:
                    ch, channel = ch_channel_map[name]
                    channel_file.write(f"{name},{ch},{channel},{url},{height},{elapsed_time},{review},{address},{tv}\n")
                else:
                    waiting_file.write(f"{name},{url}\n")

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
process_chanel_and_waiting()
"""
def backup_chanel(chanel_path='txt/channel.txt', backup_path='txt/channel_finished.txt'):
    
    将chanel.txt复制到chanel_finished.txt进行备份。

    参数:
    - chanel_path: 原始文件路径，默认为'txt/channel.txt'。
    - backup_path: 备份文件路径，默认为'txt/channel_finished.txt'。

    无返回值。
    
    try:
        # 打开源文件（chanel.txt）用于读取
        with open(chanel_path, 'r', encoding='utf-8') as chanel_file:
            # 打开备份文件（channel_finished.txt）用于写入
            with open(backup_path, 'w', encoding='utf-8') as backup_file:
                # 将源文件内容逐行复制到备份文件
                for line in chanel_file:
                    backup_file.write(line)

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
backup_chanel()
"""