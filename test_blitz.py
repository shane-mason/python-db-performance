
import os
import blitzdb

class Entry(blitzdb.Document):
    pass


class BlitzTest():

    def __init__(self, filepath, targets):
        self.path = filepath
        self.db = blitzdb.FileBackend(self.path)
        self.db.autoregister(Entry)
        self.targets = targets

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
        c = Entry(data)
        self.db.save(c)
        self.db.commit()

    def insert_multiple(self, data):
        for entry in data:
            self.insert_single(entry)
        self.db.commit()

    def get_one(self):
        element = self.db.get(Entry, {"slug": self.targets['get_one']})
        return element

    def get_many(self):
        elements = self.db.filter(Entry, {"status": self.targets['get_many']})
        #print("Get many: %s" % len(element))
        return elements

    def get_complex_and(self):
        elements = self.db.filter(Entry, {"first_name": self.targets['get_complex_and'][0], "gender" : self.targets['get_complex_and'][1]})
        return elements

    def get_complex_or(self):
        elements = self.db.filter(Entry, {"$or":[{self.targets['get_complex_or'][0]}, {"first_name": self.targets['get_complex_or'][1]}]})
        return elements

    def get_nested(self):
        elements = self.db.filter(Entry, {"address.city" : self.targets['get_nested']})
        return elements

    def update_one(self):
        item = self.db.get(Entry, {"gid": self.targets['update_one']})
        item.first_name = "Awesome"
        self.db.save(item)
        self.db.commit()
        return item

    def update_many(self):
        results = self.db.filter(Entry, {'gender' : self.targets['update_many']})
        for result in results:
            result.first_name = "Girl"
            self.db.save(result)
        self.db.commit()
        return results

    def delete_one(self):
        entries = self.db.filter(Entry, {"gid": self.targets['delete_one']})
        entries.delete()
        self.db.commit()

    def delete_many(self):
        results = self.db.filter(Entry, {'gender' : self.targets['update_many']})
        results.delete()
        self.db.commit()

    def empty(self):
        entries = self.db.filter(Entry,{})
        entries.delete()
        self.db.commit()