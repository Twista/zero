import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv/lib/python3.9/site-packages'))

import app  # Replace with your actual application
import serverless_wsgi



# If you need to send additional content types as text, add then directly
# to the whitelist:
#
# serverless_wsgi.TEXT_MIME_TYPES.append("application/custom+json")

def handler(event, context):
    return serverless_wsgi.handle_request(app.app, event, context)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True,
        threaded=True,
    )
