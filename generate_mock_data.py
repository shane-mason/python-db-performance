
from document_generator import DocumentGenerator
from test_config import config
import random
import shelve

if __name__ == "__main__":

    output_dir = config['mock_directory']
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
            users.append(config['target_values']['get_nested'])
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
        random.choice(documents)['slug'] = config['target_values']['get_one'] # "a-very-unique-slug"
        random.choice(documents)['slug'] = config['target_values']['update_one'] #"another-very-unique-slug"
        random.choice(documents)['slug'] = config['target_values']['delete_one'] #"third-very-unique-slug"

        file_name = "%s/%s.%i" % (output_dir, output_name_prefix, count)

        print(file_name)
        with shelve.open(file_name) as db:
            db['todos'] = documents

