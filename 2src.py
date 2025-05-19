import nemo.collections.asr as nemo_asr
from pathlib import Path
import librosa
from tqdm import tqdm
import os
import time as t
from nemo.utils import logging as nemo_logging

nemo_logging.set_verbosity(nemo_logging.CRITICAL)

asr_model = nemo_asr.models.ASRModel.from_pretrained(model_name="nvidia/parakeet-tdt-0.6b-v2")

# Define the audio path and target sample rate
audio_path_base = Path.cwd() / "Audio" 
clean_text_path_base = Path.cwd() / "Clean_Text" 
script_path_base = Path.cwd() / "Script"

os.makedirs(script_path_base, exist_ok=True)
os.makedirs(clean_text_path_base, exist_ok=True)

target_sr = asr_model.preprocessor._cfg.sample_rate

# Define chunk size in seconds

def transcribe_audio(audio_data, name, chunk_size_seconds=720, target_sr=16000, save_clean_text=True):
    """
    Transcribe audio data to text with timestamps.
    
    Args:
        audio_data: numpy array containing the audio data
        name: name of the output file
        chunk_size_seconds: size of audio chunks in seconds
        target_sr: target sample rate
        save_src: whether to save SRT file
        save_clean_text: whether to save clean text file
    """
    chunk_size_samples = int(chunk_size_seconds * target_sr)

    # Process audio in chunks
    clean_transcriptions = [] if save_clean_text else None
    segment_timestamps = []
    word_timestamps = []
    char_timestamps = []

    for i in tqdm(range(0, len(audio_data), chunk_size_samples)):
        chunk = audio_data[i:i + chunk_size_samples]
        output = asr_model.transcribe([chunk], timestamps=True, batch_size=1)
        
        # Adjust timestamps by adding the chunk's start time
        chunk_start_time = i / target_sr
        for word_stamp in output[0].timestamp['word']:
            word_stamp['start'] += chunk_start_time
            word_stamp['end'] += chunk_start_time
            word_timestamps.append(word_stamp)
            # clean_transcriptions.append(word_stamp['word']) if save_clean_text else None
        
        for segment_stamp in output[0].timestamp['segment']:
            segment_stamp['start'] += chunk_start_time
            segment_stamp['end'] += chunk_start_time
            segment_timestamps.append(segment_stamp)
        
        for char_stamp in output[0].timestamp['char']:
            char_stamp['start'] += chunk_start_time
            char_stamp['end'] += chunk_start_time
            char_timestamps.append(char_stamp)

    srt_file_path = script_path_base/ f"{name}.srt"
    clean_transcriptions_path = clean_text_path_base/ f"{name}.txt"




    with open(srt_file_path, "w", encoding="utf-8") as f:
        for i, stamp in enumerate(segment_timestamps):
            start_time_formatted = format_srt_time(stamp['start'])
            end_time_formatted = format_srt_time(stamp['end'])
            text = stamp['segment']
            
            f.write(f"{i + 1}\n")
            f.write(f"{start_time_formatted} --> {end_time_formatted}\n")
            f.write(f"{text}\n\n") # SRT entries are separated by a blank line

    if save_clean_text:
        with open(clean_transcriptions_path, "w", encoding="utf-8") as f:
            for i, stamp in enumerate(segment_timestamps):
                text = stamp['segment']
                f.write(f"{text}\n") # SRT entries are separated by a blank line

def format_srt_time(seconds: float) -> str:
    """Converts seconds to HH:MM:SS,ms SRT time format."""
    millisec = int((seconds % 1) * 1000)
    total_seconds = int(seconds)
    sec = total_seconds % 60
    total_minutes = total_seconds // 60
    minute = total_minutes % 60
    hour = total_minutes // 60
    return f"{hour:02d}:{minute:02d}:{sec:02d},{millisec:03d}"


if __name__ == "__main__":
    audios_names = os.listdir(audio_path_base)
    # audios_names = audios_names[0:1]
    total_duration_seconds = 0.0

    start_time = t.time()

    for audio_filename in tqdm(audios_names):
        current_audio_path = audio_path_base / audio_filename
        
        save_name = audio_filename.split(".")[0]
        # Load audio; librosa.load returns a tuple (y, sr)
        audio_data, sr_loaded = librosa.load(current_audio_path, sr=target_sr, mono=True)
        
        # Calculate duration of the current audio file
        duration_current_audio = len(audio_data) / sr_loaded
        total_duration_seconds += duration_current_audio
        
        # Call transcribe_audio with just the audio data
        transcribe_audio(audio_data, save_name, save_clean_text=1)

    # After processing all files, print the total duration
    # Formatting the duration into H:M:S
    hours = int(total_duration_seconds // 3600)
    minutes = int((total_duration_seconds % 3600) // 60)
    seconds_frac = total_duration_seconds % 60  # This will be float if total_duration_seconds is float
    
    # Using f-string for formatted output in Traditional Chinese
    print(f"Total Audio time: {hours:02d} hours {minutes:02d} minutes {seconds_frac:.2f} seconds")
    print(f"Cost: {t.time() - start_time:.2f} seconds")