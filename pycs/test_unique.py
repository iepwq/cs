def deduplicate_test_file(input_file='txt/test.txt', output_file='txt/test_unique.txt'):
    # 存储去重后的数据，以URL为键，元组（name, height, elapsed_time）为值
    unique_data = {}

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                try:
                    name, url, height, elapsed_time = line.split(',')[:4]
                except ValueError:
                    print(f"跳过格式异常的行：{line}")
                    continue

                # 将URL转换为小写并作为键
                #url_key = url.lower()
                url_key = url

                # 如果URL尚未出现，或者当前行的height值小于已存储的高度，更新存储的数据
                if url_key not in unique_data or (height.isnumeric() and int(height) < int(unique_data[url_key][1])):
                    unique_data[url_key] = (name, height, elapsed_time)

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

    # 将去重后的数据写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for url_key, (name, height, elapsed_time) in unique_data.items():
                file.write(f"{name},{url_key},{height},{elapsed_time}\n")

    except IOError as e:
        print(f"文件操作失败: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 示例调用
deduplicate_test_file()
