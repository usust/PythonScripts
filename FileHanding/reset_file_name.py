import os
import random
import string

def random_filename(length):
    """生成指定长度的随机文件名，只包含字母和数字"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def rename_files(folder_path, name_length=8):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    used_names = set()

    for filename in files:
        ext = os.path.splitext(filename)[1]  # 保留后缀名
        new_name = random_filename(name_length)
        # 避免重名
        while new_name in used_names:
            new_name = random_filename(name_length)
        used_names.add(new_name)

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name + ext)

        os.rename(old_path, new_path)
        print(f"{filename} -> {new_name + ext}")

if __name__ == "__main__":
    folder = "/Users/lyu/Code/GitHub/PythonScripts/10/mails"  # 修改为你的目录路径
    name_len = 20  # 修改为你想要的文件名长度
    rename_files(folder, name_len)
