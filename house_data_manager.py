import pymongo
import abc
import json
import copy
from bson import json_util
from bson.objectid import ObjectId

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

class LocalMongoDB:

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
                self._mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
            
            if self._mongo_client and (not self._house_db):
                self._house_db = self._mongo_client["houseDB"] # choose db

            if self._house_db and (not self._house_info_coll):
                self._house_info_coll = self._house_db["house_info"]

            # connect fail
            if not self._house_info_coll:
                return False
        
        return True

    def insert_house_data(self, data):
        if not isinstance(data, HouseInfo):
            return False

        if not self.connect_db():
            return False

        if self._house_info_coll:
            data_dict = data.to_dict()
            result = self._house_info_coll.insert_one(data_dict)
            if result: # insert success
                return data_dict
            else:
                return None
            
    def get_house_list(self):
        if not self.connect_db():
            return False

        # get all documents under the collection
        cursor = self._house_info_coll.find({}) 

        ret = [x for x in cursor]
        return ret

    def update_house_data(self, data):
        if not self.connect_db():
            return False

        id = data._id

        result = self._house_info_coll.find_one_and_replace({'_id': ObjectId(id)}, data)
        if result:
            return True
        else:
            return False

    def del_house_data(self, id):
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



class CloudDB:
    def insert_house_data():
        pass

    def get_house_list():
        pass


def serialize_object(obj):
    return json_util.dumps(obj, indent=4, ensure_ascii=False)


LocalMongoDB().del_house_data("6051e48da44f430519627413")