# Audio2Text

A Python-based audio transcription tool that converts audio files to text using NVIDIA's Parakeet TDT 0.6B V2 model. The tool supports both CPU and MLX (Apple Silicon) versions of the model.

## Features

- Audio to text transcription with word-level timestamps
- Support for long audio files through chunking
- Generates both SRT subtitle files and clean text output
- Compatible with NVIDIA GPU and Apple Silicon (MLX) versions
- Efficient audio processing with librosa
- Progress tracking with tqdm

## Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (for NVIDIA version)
- Apple Silicon Mac (for MLX version)

## Installation

### 1. Create and activate a virtual environment using uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new virtual environment
uv venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 2. Install dependencies

For NVIDIA GPU version:
```bash
uv pip install -r requirements.txt
```

For Apple Silicon (MLX) version:
```bash
uv pip install -r requirements.txt
```

## Project Structure

```
Audio2Text/
├── Audio/              # Input audio files
├── Clean_Text/         # Generated clean text files
├── Script/            # Generated SRT subtitle files
├── Urls/              # URL storage for audio sources
├── 2src.py            # Main transcription script
├── download_yt.py     # YouTube download utility
└── download_ytpl.py   # YouTube playlist download utility
```

## Usage

1. Place your audio files in the `Audio/` directory.

2. Run the transcription script:
```bash
python 2src.py
```

The script will:
- Process all audio files in the `Audio/` directory
- Generate SRT subtitle files in the `Script/` directory
- Create clean text files in the `Clean_Text/` directory

## Model Information

### NVIDIA Version
- Model: [nvidia/parakeet-tdt-0.6b-v2](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2)
- Architecture: FastConformer-TDT
- Parameters: 600M
- Features:
  - Word-level timestamp predictions
  - Automatic punctuation and capitalization
  - Robust performance on spoken numbers and song lyrics

### MLX Version (Apple Silicon)
- Model: [senstella/parakeet-tdt-0.6b-v2-mlx](https://huggingface.co/senstella/parakeet-tdt-0.6b-v2-mlx)
- Optimized for Apple Silicon
- Same features as the NVIDIA version

## Performance

The model achieves excellent performance across various datasets:
- LibriSpeech (clean): 1.69% WER
- LibriSpeech (other): 3.19% WER
- TEDLIUM-v3: 3.38% WER
- VoxPopuli: 5.95% WER

## License

This project uses the NVIDIA Parakeet model which is licensed under CC-BY-4.0.

## Contributing

Feel free to submit issues and enhancement requests! 
