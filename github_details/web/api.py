from flask import Blueprint
from flask_restplus import Api

from github_details.details.api import api as details

api_v1 = Blueprint('api', __name__, url_prefix='/users')
api = Api(api_v1,
          version='1.0.0',
          title='Github HTTP API endpoint',
          validate=True)

api.add_namespace(details)