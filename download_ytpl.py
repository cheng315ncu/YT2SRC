from pytubefix import Playlist, YouTube
from pydub import AudioSegment
import os
from pathlib import Path
from tqdm import tqdm

def download_youtube_audio_as_wav(youtube_url, output_folder='output_audio', filename='audio'):
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
    
    mp4_audio.export(wav_file_path, format="wav")
    # Optional: Remove the original downloaded file
    os.remove(downloaded_file)
    return mp4_audio

def download_and_convert_playlist(youtube_playlist_url, output_folder='output_audio'):
    # Step 1: Get the playlist from the given URL
    playlist = Playlist(youtube_playlist_url)
    
    print(f"Found {len(playlist.video_urls)} videos in the playlist: {youtube_playlist_url}")
    
    # Step 2: Download and convert each video in the playlist
    for num, video_url in enumerate(tqdm(playlist.video_urls)):
        filename = f"Video_{num + 1}"
        download_youtube_audio_as_wav(video_url, output_folder, filename)

# Example usage
save_dir = Path.cwd() / "Audio"
os.makedirs(save_dir, exist_ok=True)

# Provide the playlist URL here
playlist_url = 'https://www.youtube.com/playlist?list=PLUl4u3cNGP62A-ynp6v6-LGBCzeH3VAQB'
download_and_convert_playlist(playlist_url, save_dir)
