import os


class Config:
    APP_NAME = 'github_details'

    DEBUG = False
    TESTING = False


def resolve_config():
    return {
        'local': Config()
    }.get(os.environ.get('CLOUD_ENVIRONMENT', 'local').lower())
