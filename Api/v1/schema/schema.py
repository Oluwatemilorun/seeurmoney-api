from graphene import ObjectType, Field, Schema
from .infrastructure import Infrastructure
from .category import Category
from .location import Location
from .save_query import SaveQuery
from .suggest_infrastructure import SuggestInfrastructure
from .create_infrastructure import CreateInfrastructure
from .create_category import CreateCategory
from .fetch_category import FetchCategory
from .fetch_infrastructure import FetchInfrastructure

class Query(ObjectType):
    infrastructure = Field(Infrastructure)
    category = Field(Category)
    location = Field(Location)

class MyMutation(ObjectType):
    save_Query = SaveQuery.Field()
    suggest_Infrastructure = SuggestInfrastructure.Field()
    create_Infrastructure = CreateInfrastructure.Field()
    create_Category = CreateCategory.Field()
    fetch_Category = FetchCategory.Field()
    fetch_Infrastructure = FetchInfrastructure.Field()

schema = Schema(query=Query, mutation=MyMutation)