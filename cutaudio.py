import os
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import time
from pydub import AudioSegment

# Initialize the pipeline
inference_pipeline = pipeline(
    task=Tasks.speech_timestamp,
    model='iic/speech_timestamp_prediction-v1-16k-offline',
    model_revision="v2.0.4",
    output_dir='./tmp')


# Specify the directories
audio_folder = "/cut"
text_folder = "/output1"
output_folder = "/final"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to remove quotes from the text and overwrite the original text file
def remove_quotes_and_overwrite(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Normalize quotation marks to English
    text = text.replace('“', '"').replace('”', '"')
    modified_text = ""
    quotes = []
    in_quote = False
    start_index = 0
    char_count = 0  # Initialize the count of Chinese characters only

    # Iterate through the text
    for i, char in enumerate(text):
        if char == '"':
            if not in_quote:
                in_quote = True
                start_index = char_count  # Mark start index by number of Chinese characters encountered
            else:
                quotes.append((start_index, char_count))
                in_quote = False
        elif '\u4e00' <= char <= '\u9fff':  # Check if the character is a Chinese character
            modified_text += char  # Append only Chinese characters
            char_count += 1  # Increment Chinese character count

    # Overwrite the original file with text excluding non-Chinese characters
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_text)

    return modified_text, quotes

# Process each audio file in the directory
for audio_filename in os.listdir(audio_folder):
    if audio_filename.endswith('.wav'):
        wav_file = os.path.join(audio_folder, audio_filename)
        # Replace '.wav' suffix with '.txt' in the filename, ensuring it's only the suffix
        if audio_filename.endswith('.wav'):
            text_filename = audio_filename[:-4] + '.txt'
        text_file = os.path.join(text_folder, text_filename)
        
        # Check if the corresponding text file exists
        if os.path.exists(text_file):
            # Load the audio file
            audio = AudioSegment.from_wav(wav_file)

            # Modify the text file and identify quotes
            modified_text, quote_positions = remove_quotes_and_overwrite(text_file)
            print("Processing file:", wav_file)
            print("Identified quote positions:", quote_positions)

            # Start timing the process
            start_time = time.time()

            # Run the pipeline with the modified text
            try:
                rec_result = inference_pipeline(input=(wav_file, modified_text), data_type=("sound", "text"))
                print("ASR and timestamp results:", rec_result)
            except Exception as e:
                print(f"Error running the pipeline on {wav_file}: {e}")
                rec_result = []

                                    # Extract and save the audio for identified quotes
            for start, end in quote_positions:
                start_idx = max(0, start)  # Adjust index to capture the starting character
                end_idx = min(end, len(rec_result[0]['timestamp']) - 1)  # Ensure index is within bounds
                if start_idx < len(rec_result[0]['timestamp']) and end_idx < len(rec_result[0]['timestamp']):
                    start_time_ms = rec_result[0]['timestamp'][start_idx][0]
                    # Adjust end time to use the end time of the character before the end_idx
                    if end_idx > 0:  # Check if there is a previous character to reference
                        end_time_ms1 = rec_result[0]['timestamp'][end_idx][1]
                        end_time_ms2 = rec_result[0]['timestamp'][end_idx][0]
                        end_time_ms = (end_time_ms1 + end_time_ms2) / 2.0

                    else:
                        end_time_ms = rec_result[0]['timestamp'][end_idx][0]  # If not, use the start of the first character
                    quote_audio = audio[start_time_ms:end_time_ms]
                    # Generate output filename using the original file's base name and quote position
                    quote_filename = f"{os.path.splitext(audio_filename)[0]}_quote_{start}_{end}.wav"
                    output_path = os.path.join(output_folder, quote_filename)
                    quote_audio.export(output_path, format="wav")
                    print(f"Exported audio for quote from {start + 1} to {end} to {output_path}")

            # Calculate and print the processing time
            end_time = time.time()
            print(f"Processing time for {wav_file}: {end_time - start_time} seconds")
        else:
            print(f"No corresponding text file found for {wav_file}")
