import pydblite

class PyDBLiteTest():

    def __init__(self, filepath, targets):
        self.path = filepath
        self.targets = targets
        self.db = pydblite.Base(self.path)
        if not self.db.exists():
            self.db.create('permissions', 'slug', 'created', 'due', 'priority', 'status', 'projects', 'labels', 'title', "details")
        else:
            self.db.open()

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
        for item in data:
            self.db.insert(
                permissions=item["permissions"],
                slug=item["slug"],
                created=item["created"],
                due=item["due"],
                priority=item["priority"],
                status=item["status"],
                title=item["title"],
                details=item["details"],
                projects=item["projects"],
                labels=item["labels"])

        self.db.commit()

    def get_one(self):
        element = self.db(slug=self.targets["get_one"])
        return element

    def get_many(self):
        elements = self.db(priority="minor")
        print("many: ", len(elements))
        return elements

    def get_complex_and(self):
        elements = self.db(priority="blocker", status="blocked")
        print("and: ", len(elements))
        return elements

    def get_complex_or(self):
        elements = [r for r in self.db if r['status'] == "closed" or r['priority'] == 'critical']
        return elements

    def get_nested(self):
        elements = [r for r in self.db if r['permissions']['owner'] == self.targets["get_nested"]]
        return elements

    def update_one(self):
        self.db.update(self.db(slug=self.targets["update_one"]), status="completed")
        self.db.commit()
        return None

    def update_many(self):
        for rec in self.db(priority="minor"):
            self.db.update(rec, status="closed")
        self.db.commit()
        return None

    def delete_one(self):
        deleted = self.db.delete(self.db(slug=self.targets["delete_one"]))
        self.db.commit()
        return deleted

    def delete_many(self):
        deleted = self.db.delete(self.db(status='none'))
        self.db.commit()
        return deleted

    def empty(self):
        deleted = self.db.delete(self.db())
        self.db.commit()
        return deleted
