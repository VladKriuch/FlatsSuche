from pymongo import MongoClient
import pymongo

# DOCS https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection


class PyMongoDBManager:
    def __init__(
            self,
            connection_string="",
            target_db_name="",
            target_collection_name="",
            required_fields=[]
    ):
        self.CONNECTION_STRING = connection_string
        self.client = MongoClient(self.CONNECTION_STRING)
        self.db = self.client[target_db_name]
        self.collection = self.db[target_collection_name]
        self.required_fields = required_fields

    def add_one(self, item_data: dict):
        if len(self.required_fields) != 0:
            for field in self.required_fields:
                if field not in item_data:
                    raise KeyError(
                        f"REQUIRED FIELD MUST BE IN ITEM DATA"
                        f"required field: {field}"
                        f"item_data: {item_data}"
                    )

        self.collection.insert_one(item_data)

    def get_many(self, filter_by={}):
        items = self.collection.find(filter_by)
        return items

    def get_first(self, filter_by={}):
        first_item = self.collection.find_one(filter_by)
        return first_item

    def edit_one(self, filter_by, set_to):
        self.collection.update_one(filter_by, {'$set': set_to})

    def remove_one(self, filter_by):
        self.collection.delete_one(filter_by)

    def is_in_db(self, filter_by):
        item = self.get_first(filter_by)
        return item is not None


# if __name__ == "__main__":
#     # Get the database
#     manager = PyMongoDBManager()
#     dbname = manager.get_database()
#     print(dbname)
#     print("COLLECTION")
#     collection = dbname['users_collection']
#
#     item_1 = {
#         # "_id": "U1IT00001",
#         "item_name": "Blender",
#         "max_discount": "10%",
#         "batch_number": "RR450020FRG",
#         "price": 340,
#         "category": "kitchen appliance"
#     }
#
#     item_2 = {
#         # "_id": "U1IT00002",
#         "item_name": "Egg",
#         "category": "food",
#         "quantity": 12,
#         "price": 36,
#         "item_description": "brown country eggs"
#     }
#     # INSERT MANY
#     # collection.insert_many([item_1, item_2])
#     collection.insert_one(item_1)  # insert one
#     collection.insert_one(item_2)  # insert one
#
#     item_details = collection.find({})
#     for item in item_details:
#         # This does not give a very readable output
#         print(item['item_name'])
#
#     item_details = collection.find({"category": "cars"})  # finds all where category = food
#     oneDetail = collection.find_one({})
#     result = dbname.users_collection.update_one({'_id': oneDetail.get('_id')}, {'$set': {"category": "cars"}})
#     collection.delete_many({})
