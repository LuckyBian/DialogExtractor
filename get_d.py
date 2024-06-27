import os

# 文件夹路径
audio_folder = '/home/weizhenbian/web/cut'  # wav音频文件夹
text_folder = '/home/weizhenbian/web/text_from_audio'  # 音频对应的文本文件夹
dialogue_folder = '/home/weizhenbian/web/getweb/texts'  # 人物对白文本文件夹
modified_folder = '/home/weizhenbian/web/output1'  # 修改后的文本文件夹，包含引号的对白
dialogue_only_folder = '/home/weizhenbian/web/output2'  # 只包含对白的文本文件夹

# 确保输出文件夹存在
os.makedirs(modified_folder, exist_ok=True)
os.makedirs(dialogue_only_folder, exist_ok=True)

# 读取对白文件列表并存储对白内容
dialogue_texts = []
for filename in os.listdir(dialogue_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(dialogue_folder, filename), 'r', encoding='utf-8') as file:
            dialogue_texts.append(file.read().strip())

# 检查text_from_audio文件夹中的文件并处理
for filename in os.listdir(text_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(text_folder, filename), 'r', encoding='utf-8') as file:
            content = file.read().strip()
        
        # 找出所有包含的对白片段
        included_dialogues = [dialogue_text for dialogue_text in dialogue_texts if dialogue_text in content]
        
        if included_dialogues:
            # 保留并更新包含对白的文本文件，对白部分加引号
            modified_content = content
            for dialogue in included_dialogues:
                modified_content = modified_content.replace(dialogue, f'“{dialogue}”')
            
            with open(os.path.join(modified_folder, filename), 'w', encoding='utf-8') as mod_file:
                mod_file.write(modified_content)
            
            # 另一个文件只包含对白，不加引号
            with open(os.path.join(dialogue_only_folder, filename), 'w', encoding='utf-8') as dial_file:
                dial_file.write('\n'.join(included_dialogues))

print("处理完成。")
