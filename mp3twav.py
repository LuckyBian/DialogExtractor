import os
from pydub import AudioSegment

def convert_mp3_to_wav(folder_path):
    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(folder_path, filename)
            wav_path = os.path.join(folder_path, filename[:-4] + ".wav")
            
            # 转换格式
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(wav_path, format="wav")
            
            # 删除原始MP3文件
            os.remove(mp3_path)
            print(f"Converted and removed: {mp3_path}")

# 使用示例
convert_mp3_to_wav("/home/weizhenbian/web/20")
