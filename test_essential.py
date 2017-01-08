import essentialdb

class EssentialTest():

    def __init__(self, filepath, targets):
        self.path = filepath
        self.targets = targets
        self.db =  essentialdb.EssentialDB(filepath=self.path)

    @staticmethod
    def _reset(db_path):
        try:
            import glob, os
            test = "%s/*" % db_path
            r = glob.glob(test)
            for i in r:
               os.remove(i)
        except:
            print("Error on delete...")

    def insert_single(self, data):
        raise NotImplementedError

    def insert_multiple(self, data):
        self.db.insert_many(data)
        self.db.sync()

    def get_one(self):
        element = self.db.find_one({"slug": self.targets["get_one"]})
        return element

    def get_many(self):
        elements = self.db.find({"priority": "minor"})
        #print("many:", len(elements))
        return elements

    def get_complex_and(self):
        elements = self.db.find({"priority": "blocker", "status": "blocked"})
        #print("and:", len(elements))
        return elements

    def get_complex_or(self):
        elements = self.db.find({"$or": [{"status": "closed"}, {"priority": "critical"}]})
        #print("or:", len(elements))
        return elements

    def get_nested(self):
        elements = self.db.find({"permissions.owner": self.targets["get_nested"]})
        #print("nested:", len(elements))
        return elements

    def update_one(self):
        updated = self.db.update({'slug': self.targets['update_one']}, {'status' : "completed"})
        self.db.sync()
        return updated

    def update_many(self):
        updated =  self.db.update({'priority': 'minor'}, {'status' : "closed"})
        self.db.sync()
        return updated

    def delete_one(self):
        deleted = self.db.remove({'slug': self.targets["delete_one"]})
        self.db.sync()
        return deleted

    def delete_many(self):
        deleted = self.db.remove({'status': 'none'})
        self.db.sync()
        return deleted

    def empty(self):
        removed = self.db.remove()
        self.db.sync();
        return removed
