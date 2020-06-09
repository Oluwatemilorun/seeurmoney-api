from flask import Blueprint

bp = Blueprint('v1', __name__)

from Api.v1 import schema, routes