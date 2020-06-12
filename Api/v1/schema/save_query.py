from graphene import Mutation, String, Field
from .infrastructure_query_input import InfrastructureQueryInput

class SaveQuery(Mutation):
    class Arguments:
        user_id = String(required=True)
        query_input = InfrastructureQueryInput(required=True)

    query = Field(InfrastructureQueryInput)
    
    @staticmethod
    def mutate(root, info, user_id, query_input):
        return SaveQuery(query=query_input)