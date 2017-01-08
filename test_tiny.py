import os
import tinydb

class TinyTest():

    def __init__(self, filepath, targets):
        self.path = filepath
        self.targets = targets
        self.db =  tinydb.TinyDB(self.path)

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
        self.db.insert_multiple(data)

    def get_one(self):
        q = tinydb.Query()
        element = self.db.search(q.slug == self.targets['get_one'])
        return element

    def get_many(self):
        q = tinydb.Query()
        elements = self.db.search(q.priority == "minor")
        return elements

    def get_complex_and(self):
        q = tinydb.Query()
        elements = self.db.search((q.priority == "blocker") & (q.status == "blocked"))

        return elements

    def get_complex_or(self):
        q = tinydb.Query()
        elements = self.db.search((q.status == "closed") | (q.priority == "critical"))
        return elements

    def get_nested(self):
        q = tinydb.Query()
        elements = self.db.search(q.permissions.owner == self.targets['get_nested'])
        return elements

    def update_one(self):
        q = tinydb.Query()
        return self.db.update({'status' : "completed"}, q.slug == self.targets['update_one'])

    def update_many(self):
        q = tinydb.Query()
        return self.db.update({'status' : "closed"}, q.priority == "minor")

    def delete_one(self):
        q = tinydb.Query()
        return self.db.remove(q.slug == self.targets['delete_one'])

    def delete_many(self):
        q = tinydb.Query()
        return self.db.remove(q.status == "none")

    def empty(self):
        return self.db.purge()



import timeit
#test = TinyTest('dbfiles/tiny-10000k', {})
#print(len(test.db))
#def get_many():
#    test.get_many()


#res = timeit.timeit(stmt="test.get_many()", number=30, setup="from __main__ import test")
#print(res)