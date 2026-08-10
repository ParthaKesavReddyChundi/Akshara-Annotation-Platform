import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit_app"))

crash_log = ""
try:
    crash_log += "Importing sys...\n"
    import sys
    crash_log += "Importing backend.core.config...\n"
    import backend.core.config
    crash_log += "Importing database.database...\n"
    import database.database
    crash_log += "Importing backend.main...\n"
    from backend.main import app
    crash_log += "Successfully imported app!\n"
except Exception as e:
    import traceback
    crash_log += traceback.format_exc()
    
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': crash_log.encode('utf-8'),
        })
