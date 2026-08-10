import os
import sys
import argparse
from urllib.request import urlretrieve

# Setup Python path
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

def init_cloudinary():
    if not settings.CLOUDINARY_URL:
        print("[ERROR] CLOUDINARY_URL is not set in the environment or .env file.")
        sys.exit(1)
    # The cloudinary package automatically parses CLOUDINARY_URL from the env var.
    # We just explicitly set it if it's in our pydantic settings.
    os.environ["CLOUDINARY_URL"] = settings.CLOUDINARY_URL
    cloudinary.config()

def upload_audio():
    init_cloudinary()
    db = SessionLocal()
    
    try:
        # Find audio files without a Cloudinary public ID
        pending_files = db.query(AudioFile).filter(AudioFile.cloudinary_public_id.is_(None)).all()
        if not pending_files:
            print("[INFO] No pending audio files to upload to Cloudinary.")
            return

        print(f"[INFO] Found {len(pending_files)} audio file(s) to upload.")

        for audio in pending_files:
            print(f"\nProcessing {audio.original_filename} (ID: {audio.id})")
            
            # 1. Determine local path or download from existing audio_url
            local_path = None
            is_temp = False
            
            if audio.audio_url and audio.audio_url.startswith("http"):
                # Download temporarily
                print(f"  Downloading from existing URL: {audio.audio_url[:50]}...")
                local_path = f"temp_{audio.id}.wav"
                urlretrieve(audio.audio_url, local_path)
                is_temp = True
            elif os.path.exists(audio.file_path):
                local_path = audio.file_path
            else:
                # Try finding it in assets
                potential_path = os.path.join(_ROOT, "assets", "audio", audio.filename)
                if os.path.exists(potential_path):
                    local_path = potential_path
                else:
                    print(f"  [ERROR] Cannot find local file or URL for {audio.filename}. Skipping.")
                    continue

            # 2. Upload to Cloudinary
            try:
                print(f"  Uploading to Cloudinary (using upload_large)...")
                response = cloudinary.uploader.upload_large(
                    local_path, 
                    resource_type="video", # Cloudinary uses 'video' for audio files
                    folder="akshara_audio"
                )
                
                public_id = response.get("public_id")
                secure_url = response.get("secure_url")
                
                if not public_id:
                    raise Exception("Cloudinary upload succeeded but returned no public_id.")

                print(f"  [SUCCESS] Uploaded as {public_id}")
                
                # 3. Update database
                audio.cloudinary_public_id = public_id
                audio.audio_url = secure_url # Cloudinary URL now acts as the primary audio_url
                db.commit()
                print("  Database record updated.")
                
            except Exception as e:
                db.rollback()
                print(f"  [ERROR] Upload failed: {e}")
                
            finally:
                if is_temp and local_path and os.path.exists(local_path):
                    os.remove(local_path)

    finally:
        db.close()
        print("\n[DONE] Upload process complete.")

if __name__ == "__main__":
    upload_audio()
