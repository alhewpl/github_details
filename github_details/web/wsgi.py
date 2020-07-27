"""
WSGI entrypoint
"""

from github_details.web.factory import (
    create_web_app, configure_uwsgi)

app = create_web_app()
configure_uwsgi(app)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8115)