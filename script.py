import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'streamlit_app'))
from database.database import SessionLocal
from database.models import AudioFile

db = SessionLocal()
audio = db.query(AudioFile).first()
if audio:
    print('file_path:', audio.file_path)
    print('id:', audio.id)
    print('cloudinary_url:', getattr(audio, 'cloudinary_url', 'N/A'))
