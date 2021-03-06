import pymongo
import json
import copy
from bson import json_util
from bson.objectid import ObjectId
from app_config import config

from GetHome import logger

class HouseInfo():
    def __init__(self):
        self.price = ""

        self.age = ""               # 屋齡
        self.house_pattern = ""     # 格局
        self.ownership_size = ""    # 權狀坪數
        
        self.floors = ""            # 樓層資訊
        self.direction = ""         # 座向
        self.apartment_complex = "" # 社區
        self.address = ""

        self.building_type = ""         # 建物類型
        self.main_building_size = ""    # 主建物坪數
        self.land_size = ""             # 土地坪數
        self.source = ""                # 資料來源

    def to_dict(self):
        # deep copy avoid data modified
        return copy.deepcopy(self.__dict__)

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)

class HouseManager:

    # singleton pattern
    _instance = None
    def __new__(cls): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
        return cls._instance

    def __init__(self):
        self._mongo_client = None
        self._house_db = None
        self._house_info_coll = None


    def connect_db(self):
        if self._house_info_coll:
            return True
        else:
            # try to connect db
            if not self._mongo_client:
                self._mongo_client = pymongo.MongoClient(config['env_vars']['MONGODB_CONN_STR'])
            
            if self._mongo_client and (not self._house_db):
                self._house_db = self._mongo_client["houseDB"] # choose db

            if self._house_db and (not self._house_info_coll):
                self._house_info_coll = self._house_db["house_info"]

            # connect fail
            if not self._house_info_coll:
                return False
        
        return True

    def insert_house_data(self, userid:str, data:dict):
        if not isinstance(data, dict):
            return False

        if not self.connect_db():
            return False

        data['userid'] = userid
        self._house_info_coll.insert_one(data)
        return data
            
    def get_house_list(self, filter:dict):
        if not self.connect_db():
            return False

        if not isinstance(filter, dict):
            raise TypeError("Expected dict type")

        # get all documents under the collection
        cursor = self._house_info_coll.find(filter)

        ret = [x for x in cursor]
        for ele in ret:
            ele['id'] = str(ele.get('_id'))
            ele.pop('_id')

        return ret

    def update_house_data(self, id:str, data:dict):
        if not isinstance(data, dict):
            return False

        if not self.connect_db():
            return False

        result = self._house_info_coll.find_one_and_update({'_id': ObjectId(id)}, {"$set":data})
        if result:
            return True
        else:
            return False

    def del_house_data(self, id:str):
        if not self.connect_db():
            return False

        cnt = self._house_info_coll.count_documents({'_id': ObjectId(id)})
        if cnt == 0:
            return True

        result = self._house_info_coll.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return True
        else:
            return False

def serialize_object(obj):
    return json_util.dumps(obj, indent=4, ensure_ascii=False)