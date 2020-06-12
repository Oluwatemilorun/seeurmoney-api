from graphene import ObjectType, String, List, Int

class Location(ObjectType):
    area_name = String()
    cordinate =  List(args={'latitude' : Int(), 'longitude' : Int()})
