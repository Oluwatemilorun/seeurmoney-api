from graphene import Mutation, String, Field, Int, List
from .category import Category
from .infrastructure import Infrastructure
from ..schema import INFRASTRUCTURE_REF

class CreateInfrastructure(Mutation):
    class Arguments:
        name = String(required=True)
        description = String()
        category = Field(Category)
        amount = Int(required=True)
        rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)})
        keyword  = String(required=True)

    new_infrastructure = Field(Infrastructure)

    @staticmethod
    def mutate(root, info, name, description, category, amount, rules, keyword):
        try:
            infrastructure = INFRASTRUCTURE_REF.add({
                name : name,
                description : description,
                category : category,
                amount : amount,
                rules : rules, 
                keyword : keyword
            })
            new_infrastructure = INFRASTRUCTURE_REF.document(infrastructure.id).get()
            return CreateInfrastructure(new_infrastructure=new_infrastructure)

        except Exception as e:
            return f'An Error Occured!'
