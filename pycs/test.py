import concurrent.futures
import av
import time

# 读取txt/merge.txt文件
with open('txt/merge.txt', 'r', encoding='utf-8') as f:
    iptv_data = f.readlines()

# 定义处理URL的函数，尝试获取视频高度，最多重试3次
def process_url(line, retries=3, retry_interval=20):
    """
    处理给定的URL，尝试打开并获取视频流的高度，如果失败则根据重试次数进行重试。

    参数:
    - line: 包含名称和URL的字符串，两者之间以逗号分隔。
    - retries: int, 在尝试打开URL失败时进行的最大重试次数，默认为1。
    - retry_interval: int, 两次重试之间等待的时间间隔（秒），默认为3。

    返回值:
    - bool, 如果成功处理URL则返回True，否则返回False。
    """
    name, url = line.strip().split(',')  # 解析输入的line字符串
    retry_count = 0

    while retries > 0:
        start_time = time.time()  # 记录处理开始时间

        try:
            container = av.open(url)  # 尝试打开URL
            stream = next(s for s in container.streams if s.type == 'video')  # 获取视频流

            height = stream.height  # 获取视频高度

            if height > 0:  # 如果高度有效
                end_time = time.time()  # 记录处理结束时间
                elapsed_time = end_time - start_time  # 计算处理耗时
                # 打印和写入成功处理的信息
                print(f"测试 {name}, {url} 成功，{height}P，用时 {elapsed_time:.2f} 秒")
                with open('txt/test.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{name},{url},{height},{elapsed_time:.2f}\n')
                return True  # 标记处理成功

            else:
                # 如果视频高度无效，则抛出异常
                raise ValueError("Height is not greater than 0")

        except Exception as e:
            end_time = time.time()  # 记录处理结束时间
            elapsed_time = end_time - start_time  # 计算处理耗时
            retry_count += 1  # 重试计数增加

            # 如果还有重试次数，则打印失败信息并进行重试
            if retries > 1:
                print(f"第{retry_count}次测试 {name}, {url} 失败，用时 {elapsed_time:.2f} 秒:\n {e}")
                print(f"将在{retry_interval}秒后进行第{retry_count + 1}次尝试...")
                time.sleep(retry_interval)  # 等待重试间隔时间

        retries -= 1  # 重试次数减少

    # 如果所有重试都失败，则打印失败信息并记录到文件
    print(f"重试{retry_count}次后仍失败：{name}, {url}，共耗时 {elapsed_time:.2f} 秒")
    with open('txt/over.txt', 'a', encoding='utf-8') as f:
        f.write(f'{name},{url}\n')
    return False  # 标记处理失败


# 遍历读取的内容，通过多线程获取每个URL的高度信息
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures_list = []  # 存储Future对象的列表

    total_tasks = len(iptv_data)
    completed_tasks = 0
    successful_tasks = 0

    for i, line in enumerate(iptv_data, start=1):
        future = executor.submit(process_url, line)
        futures_list.append(future)

        def update_status(future):
            global completed_tasks, successful_tasks
            result = future.result()
            completed_tasks += 1
            if result:
                successful_tasks += 1
            print(f"进度：已处理 {completed_tasks}/{total_tasks} 项任务（完成率：{completed_tasks / total_tasks * 100:.2f}%，成功率：{(successful_tasks / completed_tasks) * 100:.2f}%，剩余 {total_tasks - completed_tasks} 项任务，成功 {successful_tasks} 项，失败 {completed_tasks - successful_tasks} 项）")

        future.add_done_callback(update_status)

# 等待所有任务完成
concurrent.futures.wait(futures_list)
print("所有任务已完成！")
