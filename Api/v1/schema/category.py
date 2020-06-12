from graphene import ObjectType, ID, String, List, Field, Int
from .infrastructure import Infrastructure

class Category(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    description = String()
    rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)})
    infrastructure = List(Field(Infrastructure))

