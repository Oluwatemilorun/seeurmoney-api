from graphene import ObjectType, ID, Int, String, List, Field
from .category import Category

class Infrastructure(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    description = String()
    category = Field(Category)
    amount = Int(required=True)
    rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)})
    keyword  = String(required=True)