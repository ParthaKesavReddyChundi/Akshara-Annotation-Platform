import traceback
import os
import sys

# Minimal ASGI app that shows us what path Vercel is sending requests to
async def app(scope, receive, send):
    if scope['type'] == 'http':
        path = scope.get('path', 'unknown')
        qs = scope.get('query_string', b'').decode()
        method = scope.get('method', 'unknown')
        headers = dict(scope.get('headers', []))
        host = headers.get(b'host', b'unknown').decode()
        
        body = f"METHOD: {method}\nPATH: {path}\nQUERY: {qs}\nHOST: {host}\nRAW_PATH: {scope.get('raw_path', b'').decode()}\n"
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': body.encode('utf-8'),
        })
