from graphene import InputObjectType, Field, Int, String
from .location import Location

class InfrastructureQueryInput(InputObjectType):
    location = Field(Location, required=True)
    radius = Int(default_value=50000)
    amount =  Int(required=True)
    infrastructure = String()