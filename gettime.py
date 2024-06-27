import os
from pydub import AudioSegment

def get_total_duration_wav(directory):
    total_duration = 0  # Duration in milliseconds

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            audio = AudioSegment.from_wav(filepath)
            total_duration += len(audio)

    # Convert milliseconds to hours, minutes, and seconds
    total_seconds = total_duration // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds

# Specify the directory containing WAV files
directory = '/data/weizhen/getweb2/final'
hours, minutes, seconds = get_total_duration_wav(directory)
print(f"Total Duration: {hours} hours, {minutes} minutes, and {seconds} seconds")
