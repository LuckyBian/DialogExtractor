import os
from pydub import AudioSegment
from glob import glob

# 设置你的文件夹路径
audio_folder = "/home/weizhenbian/web/20"
#text_folder = "/data/weizhen/getweb2/output2"

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
            
            # 对应的文本文件路径
            #text_file = os.path.join(text_folder, filename + '.txt')
            
            # 删除音频和文本文件
            os.remove(audio_file)
            #os.remove(text_file)
            #print(f"Deleted {audio_file} and {text_file} due to insufficient duration.")
    
    except Exception as e:
        # 如果无法导入音频文件，也删除对应的文本文件
        filename = os.path.basename(audio_file).split('.')[0]
        #text_file = os.path.join(text_folder, filename + '.txt')
        
        os.remove(audio_file)
        #if os.path.exists(text_file):
            #os.remove(text_file)
        #print(f"Deleted {audio_file} and {text_file} due to an error: {str(e)}")
