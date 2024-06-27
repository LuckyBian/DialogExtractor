import os

# 设置文件夹的路径
folder_path = '/data/weizhen/output1'

# 计算文件夹中的文件数
file_count = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])

# 计算子文件夹的数量
folder_count = len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])

print(f"There are {file_count} files in {folder_path}")
print(f"There are {folder_count} subdirectories in {folder_path}")
