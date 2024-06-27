#用来重命名
import os

def rename_files(directory):
    # 遍历指定目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):  # 确保处理的是.wav文件
            # 分割文件名，假设格式总是"数字-文字.wav"
            parts = filename.split('-')
            if len(parts) > 1:  # 确保文件名包含'-'
                new_name = parts[0] + '.wav'  # 创建新的文件名，只包含数字和.wav后缀
                old_file = os.path.join(directory, filename)
                new_file = os.path.join(directory, new_name)
                os.rename(old_file, new_file)  # 重命名文件
                print(f"Renamed '{filename}' to '{new_name}'")
            else:
                print(f"No '-' in '{filename}', skipped.")
        else:
            print(f"Skipped non-wav file '{filename}'")

# 使用示例：
# replace '/path/to/your/folder' with the actual path to the directory containing your files
rename_files('/path/to/your/folder')
