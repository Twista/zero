import os
from pprint import pprint

from src.app import create_app  # NOQA
from src.config import current_config

app = create_app(os.environ.get('APP_ENV', 'local'))

print(os.environ.get('APP_ENV'))
print(current_config)
pprint(app.url_map)

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
