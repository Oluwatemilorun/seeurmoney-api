from flask_graphql import GraphQLView
from Api.api import api
from .schema.schema import schema

api.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))