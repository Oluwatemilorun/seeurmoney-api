from firebase_admin import credentials, initialize_app, firestore

cred = credentials.Certificate('google-services.json')
default_app = initialize_app(cred)
db = firestore.client()

INFRASTRUCTURE_REF = db.collection('infrastructures')
CATEGORY_REF = db.collection('categories')