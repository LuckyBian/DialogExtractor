import os
from pydub import AudioSegment
from glob import glob

# 设置你的文件夹路径
audio_folder = "/path/to/speech/folder"

# 获取所有音频文件
audio_files = glob(os.path.join(audio_folder, "*.wav"))

for audio_file in audio_files:
    try:
        # 导入音频文件
        audio = AudioSegment.from_wav(audio_file)
        
        # 检查音频长度是否小于1秒
        if len(audio) < 1000:
            # 获取音频文件名（不含扩展名）
            filename = os.path.basename(audio_file).split('.')[0]
            
            # 删除音频和文本文件
            os.remove(audio_file)
    
    except Exception as e:
        # 如果无法导入音频文件，也删除对应的文本文件
        filename = os.path.basename(audio_file).split('.')[0]
        #text_file = os.path.join(text_folder, filename + '.txt')
        
        os.remove(audio_file)
