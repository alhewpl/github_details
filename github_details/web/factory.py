import os
from typing import Union, Dict

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from github_details.web.api import api_v1
from github_details.web.config import resolve_config
from github_details.web.middlewares import StripContentTypeMiddleware


def create_web_app(config: Union[str, Dict, None] = None) -> Flask:
    """
    Creates the Flask details using provided configuration.
    :param config: Configuration to use. If no config is defined as parameter, then value mapping from
    environment variable CLOUD_ENVIRONMENT is used. If this is not set, Local config is used.
    :return: the Flask details.
    """
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.wsgi_app = StripContentTypeMiddleware(app.wsgi_app)

    debug = os.environ.get
    app.debug = debug

    app.url_map.strict_slashes = False

    # If configuration is not defined then use CLOUD_ENVIRONMENT for configuration
    if not config:
        config = resolve_config()

    app.config.from_object(config)

    app.register_blueprint(api_v1)

    return app


def configure_uwsgi(app: Flask) -> None:
    """
    Configures uWSGI
    :param Flask app: the details to configure uWSGI for.
    """
    try:
        import uwsgi
    except ImportError:
        return
