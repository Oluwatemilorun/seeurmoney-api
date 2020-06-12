from graphene import Mutation, ID, Field
from .infrastructure import Infrastructure
from ..schema import INFRASTRUCTURE_REF

class FetchInfrastructure(Mutation):
    class Arguments:
        id = ID(required=True)

    infrastructure = Field(Infrastructure)

    @staticmethod
    def mutate(root, info, id):
        infrastructure = INFRASTRUCTURE_REF.document(id).get()
        return FetchInfrastructure(infrastructure=infrastructure)
