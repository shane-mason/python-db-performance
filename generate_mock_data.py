
from document_generator import DocumentGenerator
import random
import shelve

if __name__ == "__main__":

    output_dir = "mock-data"
    output_name_prefix = "todoshelf"
    record_counts = range(10000, 110000, 10000)
    generator = DocumentGenerator()
    generator.init_word_cache()
    generator.init_sentence_cache()

    documents = []
    users = []
    labels = []
    projects = []

    def gen_permissions():
        perm =  {
            "owner": random.choice(users),
            "contributors": []
        }

        for i in range(0, random.randint(0, 4)):
            perm["contributors"].append(random.choice(users))

        return perm

    def gen_projects():
        results = []
        for i in range(0, random.randint(0, 4)):
            results.append(random.choice(projects))
        return results

    def gen_labels():
        results = []
        for i in range(0, random.randint(0, 4)):
            results.append(random.choice(labels))
        return results

    for count in record_counts:

        for i in range(0, 1000):
            users.append(generator.gen_email())
            projects.append(generator.gen_word())
            labels.append(generator.gen_word())

        if count == record_counts[0]:
            # just do this once
            users.append("targetuser@example.com")
            random.shuffle(users)

        template = {
            "permissions": gen_permissions,
            "slug": "gid",
            "created": "integer",
            "due": "integer",
            "priority": ["none", "minor", "major", "critical", "blocker"],
            "status": ["none","started", "stopped", "open", "closed", "blocked", "completed", "resolved"],
            "projects": gen_projects,
            "labels": gen_labels,
            "title": "sentence",
            "details": "paragraph"
        }

        generator.set_template(template)
        documents = generator.gen_docs(count)

        # set target values
        random.choice(documents)['slug'] = "a-very-unique-slug"
        random.choice(documents)['slug'] = "another-very-unique-slug"
        random.choice(documents)['slug'] = "third-very-unique-slug"

        file_name = "%s/%s.%i" % (output_dir, output_name_prefix, count)

        print(file_name)
        with shelve.open(file_name) as db:
            db['todos'] = documents

