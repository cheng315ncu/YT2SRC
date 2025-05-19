from pytubefix import YouTube
from pydub import AudioSegment
import os
from pathlib import Path
import polars as pl
from tqdm import tqdm

def download_youtube_audio_as_wav(youtube_url, output_folder='output_audio', filename='audio', save_mp4=False):
    # Step 1: Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Step 2: Download audio stream using pytube
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    downloaded_file = audio_stream.download(output_path=output_folder, filename=filename + '.mp4')

    # Step 3: Convert to WAV using pydub
    mp4_audio = AudioSegment.from_file(downloaded_file, format="mp4")
    wav_file_path = os.path.join(output_folder, filename + '.wav')
    
    mp4_audio.export(wav_file_path, format="wav") if save_mp4 else None
    # Optional: Remove the original downloaded file
    os.remove(downloaded_file)
    return mp4_audio

# Example usage

save_dir = Path.cwd() / "Audio" 
os.makedirs(save_dir, exist_ok=True)

urls = pl.read_csv(Path.cwd() / "Urls" / "test.csv")
print(urls)
num_urls = len(urls["URL"])
print(f"Number of URLs: {num_urls}")

for num in tqdm(range(num_urls)):
    # Get the URL string from the DataFrame row
    url = urls["URL"][num]  # This will extract the actual URL string
    download_youtube_audio_as_wav(url, save_dir, f"video{num + 1}")
