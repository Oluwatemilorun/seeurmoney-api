from graphene import Mutation, ID, Field
from .category import Category
from ..schema import CATEGORY_REF

class FetchCategory(Mutation):
    class Arguments:
        id = ID(required=True)

    category = Field(Category)

    @staticmethod
    def mutate(root, info, id):
        category = CATEGORY_REF.document(id).get()
        return FetchCategory(category=category)
