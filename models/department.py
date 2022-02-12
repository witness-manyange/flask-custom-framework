from factory.validation import Validator
from factory.database import Database


class Department(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'departments'  # collection name

        self.fields = {
            "name": "string",
            "description": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["name", "description"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["name", "description"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, department):
        # Validator will throw error if invalid
        self.validator.validate(department, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(department, self.collection_name)
        return "Inserted Id " + res

    def find(self, department):  # find all
        return self.db.find(department, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, department):
        self.validator.validate(department, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, department,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)