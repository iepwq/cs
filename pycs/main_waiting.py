#waiting 重启程序 txt/waiting.txt + txt/finished.txt

import os

print("将 txt/waiting.txt 复制到txt/new_url.txt，并将txt/waiting.txt追加写入至txt/waiting_test.txt，最后清空txt/waiting.txt"'\n')
def copy_and_append_files():
    """
    将 txt/waiting.txt 复制到txt/merge.txt，并将txt/waiting.txt追加写入至txt/waiting_test.txt，最后清空txt/waiting.txt。
    """

    # 复制txt/waiting.txt到txt/new_url.txt
    source_path = os.path.join('txt', 'waiting.txt')
    destination_path = os.path.join('txt', 'new_url.txt')
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            with open(destination_path, 'w', encoding='utf-8') as destination_file:
                destination_file.write(source_file.read())
    except FileNotFoundError:
        print(f"源文件 {source_path} 或目标文件 {destination_path} 不存在。")

    # 追加写入txt/waiting.txt到txt/waiting_test.txt
    source_path = os.path.join('txt', 'waiting.txt')
    append_path = os.path.join('txt', 'waiting_test.txt')
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            with open(append_path, 'a', encoding='utf-8') as append_file:
                append_file.write(source_file.read())
    except FileNotFoundError:
        print(f"源文件 {source_path} 或目标文件 {append_path} 不存在。")

    # 清空txt/waiting.txt
    #source_path = os.path.join('txt', 'waiting.txt')
    try:
        with open(source_path, 'w', encoding='utf-8') as file:
            pass  # Python在'w'模式下自动清空文件
    except FileNotFoundError:
        print(f"文件 {source_path} 不存在。")

copy_and_append_files()

print("txt/waiting.txt 的内容已被复制到 txt/new_url.txt，追加到了 txt/waiting_test.txt。")


print("删除url中符号$及右边的内容后删除不是name,url格式的行；各行url比对，删除重复行数据，只保留一行，结果以name,url 的格式存入txt/merge.txt")
os.system("python merge_new_url.py")


print("检测temp 输出 txt/test.txt,失败项 txt/over.txt"'\n')
os.system("python test.py")

print("txt/test.txt 按url去重，保留height最小值，输出 txt/test_unique.txt"'\n')
os.system("python test_unique.py")

print("清空 txt/waiting.txt"'\n')
with open('txt/waiting.txt', 'w') as file:
    file.truncate(0)
print("txt/waiting.txt 已清空。")

print("时移/回看review 输出 txt/review.txt"'\n')
os.system("python review.py")

print("提取地址address 输出 txt/address.txt"'\n')
os.system("python address.py")

print("提取频道chanel 输出 txt/channel.txt,未收藏 txt/waiting.txt"'\n')
os.system("python channel.py")

print("合并merge_over 输入txt/channel.txt与txt/channel_finished.txt 并去重"'\n')
os.system("python merge_again.py")

print("复制 txt/chanel.txt 到txt/channel_finished.txt"'\n')
with open('txt/channel.txt', 'r', encoding='utf-8') as source_file:
    with open('txt/channel_finished.txt', 'w', encoding='utf-8') as destination_file:
        destination_file.write(source_file.read())
print("txt/chanel.txt 文件已备份至txt/channel_finished.txt.")

print("排序sort 输出 txt/sort.txt"'\n')
os.system("python sort.py")

print("输出finished 输出 txt/finished.txt"'\n')
os.system("python finished.py")

print("分别对 txt/over.txt 与 txt/waiting.txt 去重"'\n')
os.system("python unique.py")

print("清空临时文件 txt/waiting_test.txt"'\n')
with open("txt/waiting_test.txt", "w"):
    pass
print("已清空临时文件 txt/waiting_test.txt"'\n')

input("按回车键退出...")


