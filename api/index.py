import os
import sys

# Add the project root to sys.path so modules can be resolved correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
# Add streamlit_app as well just in case legacy modules need it
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "streamlit_app"))

try:
    from backend.main import app
except Exception as e:
    import traceback
    err = traceback.format_exc()
    
    # Create a dummy ASGI app that just returns the error
    async def app(scope, receive, send):
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': err.encode('utf-8'),
        })
