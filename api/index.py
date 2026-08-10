import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit_app"))

try:
    from backend.main import app
except Exception as e:
    import traceback
    crash_log = traceback.format_exc()
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 200,  # Use 200 so Vercel doesn't mask the body!
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': crash_log.encode('utf-8'),
        })
