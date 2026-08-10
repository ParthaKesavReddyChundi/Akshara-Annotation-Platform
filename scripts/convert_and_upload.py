import os
import sys
import subprocess

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
sys.path.insert(0, os.path.join(_ROOT, "streamlit_app"))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_ROOT, ".env"))
except ImportError:
    pass

import cloudinary
import cloudinary.uploader
from database.database import SessionLocal
from database.models import AudioFile
from backend.core.config import settings

def convert_and_upload():
    url = os.environ.get("CLOUDINARY_URL") or settings.CLOUDINARY_URL
    if not url:
        print("Missing CLOUDINARY_URL")
        return
    
    os.environ["CLOUDINARY_URL"] = url
    cloudinary.config()

    import imageio_ffmpeg
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    db = SessionLocal()
    try:
        # Get the failing audio file
        audio = db.query(AudioFile).filter(AudioFile.original_filename.like("%lecture2.wav%")).first()
        if not audio:
            print("lecture2.wav not found in database.")
            return

        if audio.cloudinary_public_id:
            print("Already uploaded to Cloudinary.")
            return

        local_path = audio.file_path
        if not os.path.exists(local_path):
            print(f"Local file missing: {local_path}")
            # check assets fallback
            potential_path = os.path.join(_ROOT, "assets", "audio", audio.filename)
            if os.path.exists(potential_path):
                local_path = potential_path
            else:
                return

        mp3_path = local_path.replace(".wav", ".mp3")
        
        if not os.path.exists(mp3_path):
            print(f"Converting {local_path} to {mp3_path}...")
            # Convert WAV to MP3 using 128kbps (high enough quality for voice, low enough size)
            subprocess.run([
                ffmpeg_exe, "-y", "-i", local_path, 
                "-codec:a", "libmp3lame", "-b:a", "128k", 
                mp3_path
            ], check=True)
            print("Conversion successful.")
        else:
            print("MP3 already exists, skipping conversion.")

        # Check new size
        size_mb = os.path.getsize(mp3_path) / (1024 * 1024)
        print(f"New MP3 size: {size_mb:.2f} MB")

        print("Uploading to Cloudinary...")
        response = cloudinary.uploader.upload_large(
            mp3_path, 
            resource_type="video",
            folder="akshara_audio"
        )
        
        public_id = response.get("public_id")
        secure_url = response.get("secure_url")
        
        print(f"Uploaded as {public_id}")
        
        # Update db
        audio.cloudinary_public_id = public_id
        audio.audio_url = secure_url
        
        # update extensions
        audio.filename = audio.filename.replace(".wav", ".mp3")
        audio.original_filename = audio.original_filename.replace(".wav", ".mp3")
        
        db.commit()
        print("Database updated!")

    finally:
        db.close()

if __name__ == "__main__":
    convert_and_upload()
