import whisper, os
from yt_dlp import YoutubeDL

model = whisper.load_model("base")

def download_audio(url: str) -> str:
    opts = {'format': 'bestaudio', 'outtmpl': '/tmp/audio.%(ext)s', 'quiet': True}
    with YoutubeDL(opts) as ydl:
        ydl.download([url])
    for ext in ['webm','mp4','m4a','mp3']:
        p = f'/tmp/audio.{ext}'
        if os.path.exists(p): return p
    return None

def transcribe(path: str) -> str:
    result = model.transcribe(path, language="ar", fp16=False)
    return result["text"]