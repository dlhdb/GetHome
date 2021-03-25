import google.oauth2.id_token
import google.auth.transport.requests
import pymongo
from bson.objectid import ObjectId
from flask_login import LoginManager, UserMixin
import json
import copy

from GetHome import logger, app
from app_config import config

def validate_google_token(token):
    CLIENT_ID = config['env_vars']['google_oauth']['CLIENT_ID']
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        decoded = google.oauth2.id_token.verify_oauth2_token(
            token, google.auth.transport.requests.Request(), CLIENT_ID)

        # ID token is valid
        return decoded
    except ValueError:
        # Invalid token
        return None


class UserMongoDB:
    # singleton pattern
    _instance = None
    def __new__(cls): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance

    def __init__(self):
        self.connect_db()

    def connect_db(self):
        mongo_client = pymongo.MongoClient(config['env_vars']['MONGODB_CONN_STR'])
        self.collection = mongo_client["houseDB"]["user"]

    def get_user(self, id):
        return self.collection.find_one({"id": id})

    def add_user(self, data_dict):
        if not isinstance(data_dict, dict):
            raise TypeError('Expected dict type')

        self.collection.insert_one(data_dict)
        return data_dict

# UserMixin class provides default implementations for the methods that 
# Flask-Login expects user objects to have.
class User(UserMixin):
    _db = UserMongoDB()

    def __init__(self, id, **kwargs):
        self.id = id
        self.__dict__.update(kwargs)
    
    @staticmethod
    def get_user(id):
        data = User._db.get_user(id)
        if data:
            return User(id=data['id'], email=data['email'])

    @staticmethod
    def add_user(user):
        if not isinstance(user, User):
            raise TypeError('Expected User type')

        User._db.add_user(user.to_dict())

    def to_dict(self):
        return  copy.deepcopy(self.__dict__) 
    def to_json(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
    return User.get_user(id)
