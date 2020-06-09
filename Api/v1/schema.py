from flask import request
from graphene import ObjectType, String, Field, Schema, List, ID, Int, Mutation, InputObjectType, Boolean
from firebase_admin import credentials, initialize_app, firestore
from graphql import GraphQLError
from dotenv import load_dotenv
import os, requests


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
default_app = initialize_app(cred)
db = firestore.client()

INFRASTRUCTURE_REF = db.collection('infrastructures')
CATEGORY_REF = db.collection('categories')


api_key = os.environ.get('API_KEY')

class Category(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    description = String()
    rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)})
    infrastructure = List(Field(Infrastructure))

class Location(ObjectType):
    area_name = String()
    cordinate =  List(args={'latitude' : Int(), 'longitude' : Int()})

class Infrastructure(ObjectType):
    id = ID(required=True)
    name = String(required=True)
    description = String()
    category = Field(Category)
    amount = Int(required=True)
    rules = List(args={'quantity' : Int(default_value=1), 'distance' : Int(default_value=1)})
    keyword  = String(required=True)

class InfrastructureQueryInput(InputObjectType):
    location = Field(Location, required=True)
    radius = Int(default_value=50000)
    amount =  Int(required=True)
    infrastructure = String()

class SaveQuery(Mutation):
    class Arguments:
        user_id = String(required=True)
        query_input = InfrastructureQueryInput(required=True)

    query = Field(InfrastructureQueryInput)
    
    @staticmethod
    def mutate(root, info, user_id, query_input):
        return SaveQuery(query=query_input)

class FetchInfrastructure(Mutation):
    class Arguments:
        id = ID(required=True)

    infrastructure = Field(Infrastructure)

    @staticmethod
    def mutate(root, info, id):
        infrastructure = INFRASTRUCTURE_REF.document(id).get()
        return FetchInfrastructure(infrastructure=infrastructure)

class FetchCategory(Mutation):
    class Arguments:
        id = ID(required=True)

    category = Field(Category)

    @staticmethod
    def mutate(root, info, id):
        category = CATEGORY_REF.document(id).get()
        return FetchCategory(category=category)

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


class SuggestInfrastructure(Mutation):
    class Arguments:
        query_input = InfrastructureQueryInput(required=True)

    results = List(Field(Infrastructure))

    @staticmethod
    def mutate(root, info, query_input):
        value = query_input['infrastructure']
        all_infrastructures = (doc.to_dict() for doc in INFRASTRUCTURE_REF.stream())
        all_categories = (doc.to_dict() for doc in CATEGORY_REF.stream())
        if value:
            if value in all_infrastructures:
                response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={query_input['location']['latitude'],query_input['location']['longitude']}&radius={query_input['radius']}&type={value['keyword']}&key=" + api_key).json()
                num_of_results = len(response['results'])
                allocated_num = int(query_input['radius'] / value['rules']['distance']) * value['rules']['quantity']
                if num_of_results > allocated_num:
                    return "Number of the infrastructure in this location meets the requirement"
                else:
                    diff_num = allocated_num - num_of_results

            elif value in all_categories:
                for infra in value['infrastructure']:
                    response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={query_input['location']['latitude'],query_input['location']['longitude']}&radius={query_input['radius']}&type={infra['keyword']}&key=" + api_key).json()
                    num_of_results = len(response['results'])
                    allocated_num = int(query_input['radius'] / infra['rules']['distance']) * infra['rules']['quantity']
                    if num_of_results > allocated_num:
                        return "Number of the infrastructure in this location meets the requirement"
                    else:
                        diff_num = allocated_num - num_of_results
            else:
                raise GraphQLError('Infrastructure doesn\'t exist!')
        else:
            for category in all_categories:
                for infra in category['infrastructure']:
                    response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={query_input['location']['latitude'],query_input['location']['longitude']}&radius={query_input['radius']}&type={infra['keyword']}&key=" + api_key).json()
                    num_of_results = len(response['results'])
                    allocated_num = int(query_input['radius'] / infra['rules']['distance']) * infra['rules']['quantity']
                    if num_of_results > allocated_num:
                        return "Number of the infrastructure in this location meets the requirement"
                    else:
                        diff_num = allocated_num - num_of_results

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