from pydub import AudioSegment
import os

# 源文件夹和目标文件夹
src_folder = '/home/weizhenbian/web/20'
dst_folder = '/home/weizhenbian/web/cut'

# 检查目标文件夹是否存在，如果不存在则创建
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

# 设定切割长度为15秒（以毫秒为单位）
segment_length = 15 * 1000

# 遍历源文件夹中的所有文件
for filename in os.listdir(src_folder):
    if filename.endswith('.wav'):  # 修改此处以适应WAV格式
        # 完整的文件路径
        path = os.path.join(src_folder, filename)
        audio = AudioSegment.from_file(path, format='wav')  # 指定格式为WAV

        # 计算可以切割成多少个完整的片段
        for i in range(len(audio) // segment_length):
            # 切割音频
            segment = audio[i * segment_length:(i + 1) * segment_length]
            # 构建新的文件名和路径
            segment_filename = f'{filename[:-4]}_part{i}.wav'  # 保存为WAV格式
            segment_path = os.path.join(dst_folder, segment_filename)
            # 导出音频
            segment.export(segment_path, format='wav')  # 导出为WAV格式

print("处理完成！")
