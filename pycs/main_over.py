#over复查程序 txt/new_url.txt + txt/finished.txt
import os

print("将 txt/over.txt 复制到txt/merge.txt"'\n' )
def copy_and_append_files():
    """
    将txt/over.txt复制到txt/merge.txt，并将txt/over.txt追加写入至txt/over_test.txt，最后清空txt/over.txt。
    """

    # 复制txt/over.txt到txt/merge.txt
    source_path = os.path.join('txt', 'over.txt')
    destination_path = os.path.join('txt', 'merge.txt')
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            with open(destination_path, 'w', encoding='utf-8') as destination_file:
                destination_file.write(source_file.read())
    except FileNotFoundError:
        print(f"源文件 {source_path} 或目标文件 {destination_path} 不存在。")

    # 追加写入txt/over.txt到txt/over_test.txt
    source_path = os.path.join('txt', 'over.txt')
    append_path = os.path.join('txt', 'over_test.txt')
    try:
        with open(source_path, 'r', encoding='utf-8') as source_file:
            with open(append_path, 'a', encoding='utf-8') as append_file:
                append_file.write(source_file.read())
    except FileNotFoundError:
        print(f"源文件 {source_path} 或目标文件 {append_path} 不存在。")

    # 清空txt/over.txt
    source_path = os.path.join('txt', 'over.txt')
    try:
        with open(source_path, 'w', encoding='utf-8') as file:
            pass  # Python在'w'模式下自动清空文件
    except FileNotFoundError:
        print(f"文件 {source_path} 不存在。")

copy_and_append_files()

print("txt/over.txt 的内容已复制到 txt/merge.txt，附加到 txt/over_test.txt，并清空了 txt/over.txt。")

print("检测temp 输出 txt/test.txt,失败项 txt/over.txt"'\n')
os.system("python test.py")

print("txt/test.txt 按url去重，保留height最小值，输出 txt/test_unique.txt"'\n')
os.system("python test_unique.py")

print("时移/回看review 输出 txt/review.txt"'\n')
os.system("python review.py")

print("提取地址address 输出 txt/address.txt"'\n')
os.system("python address.py")

print("提取频道chanel 输出 txt/channel.txt,未收藏 txt/waiting.txt"'\n')
os.system("python channel.py")

print("合并merge_finished 输入txt/channel.txt与txt/channel_finished.txt 并去重"'\n')
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

#2次失败的就没有必要再验证了
#txt/over.txt 复制给 txt/lose.txt
with open('txt/over.txt', 'r', encoding='utf-8') as source_file:
    with open('txt/lose.txt', 'a', encoding='utf-8') as destination_file:
        destination_file.write(source_file.read())
with open('txt/over.txt', 'w', encoding='utf-8') as source_file:
    print("两次检测都失败，已移至txt/lose.txt存放，不再启用！")

input("按回车键退出...")