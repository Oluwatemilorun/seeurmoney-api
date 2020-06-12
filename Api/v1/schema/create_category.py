from graphene import Mutation, String, List, Field, Int
from .infrastructure import Infrastructure
from .category import Category
from ..schema import CATEGORY_REF

class CreateCategory(Mutation):
    class Arguments:
        name = String(required=True)
        description = String()
        rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)}) 
        infrastructure = List(Field(Infrastructure))
    
    new_category = Field(Category)

    @staticmethod
    def mutate(root, info, name, description, rules, infrastructure):
        try:
            category = CATEGORY_REF.add({
                name : name,
                description : description,
                rules : rules,
                infrastructure : infrastructure
            })
            new_category = CATEGORY_REF.document(category.id).get()
            return CreateCategory(new_category=new_category)
        
        except Exception as e:
            return f'An Error Occured!'