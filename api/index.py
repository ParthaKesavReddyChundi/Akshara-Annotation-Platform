import os
import sys

# Add the project root to sys.path so modules can be resolved correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# Add streamlit_app as well just in case legacy modules need it
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit_app"))

from backend.main import app
