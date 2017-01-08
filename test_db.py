import time
from test_tiny import TinyTest
from test_essential import EssentialTest
from test_pydblite import PyDBLiteTest
import shelve
from test_config import config

TINY_DB = "dbfiles/tiny"
ESSENTIAL_DB = 'dbfiles/essential'
PYDBLITE_DB = 'dbfiles/pdblite'


class Timer():
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        # self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print('elapsed time: %f seconds' % self.secs)


def import_data(file_name):
    print(file_name)
    shelf = shelve.open(file_name, flag='r')
    data = shelf["todos"]
    shelf.close()
    return data


def time_test_nocache(klass, function_name, iterations, db_path, targets):
    elapsed = 0.0

    for i in range(iterations):
        if db_path is not None:
            inst = klass(filepath=db_path, targets=targets)
        else:
            inst = klass()
        function = getattr(inst, function_name)
        with Timer() as t:
            function()

        elapsed += t.secs

    average = elapsed / iterations
    return average


def run_tests(klass, iterations, record_counts, nocache_list, db_path, targets, outfile):
    klass._reset(db_path)

    for record_count in record_counts:
        path = "%s-%ik" % (db_path, record_count)
        result_row = []

        data = import_data("mock-data/todoshelf.%i" % record_count)
        result_row.append(len(data))

        with Timer() as t:
            if db_path is not None:
                k = klass(filepath=path, targets=targets).insert_multiple(data)
            else:
                klass().insert_multiple(data)

        result_row.append(t.secs)

        for function in nocache_list:
            print("Running %i @ %s " % (record_count, str(function)))
            result_row.append(time_test_nocache(klass, function, iterations, path, targets))

        print(result_row)
        with open(outfile, 'a') as out:
            out.write(",".join(map(str, result_row)) + "\n")




if __name__ == "__main__":

    record_counts = config['record_counts']
    target_values = config['target_values']
    basic_functions = ["get_one", "get_many", "get_complex_and", "get_complex_or", "get_nested"]

    all_functions = ["get_one", "get_many", "get_complex_and", "get_complex_or", "get_nested", "update_one",
                     "update_many", "delete_one", "delete_many"]

    run_tests(EssentialTest, config['iterations'], record_counts, all_functions, ESSENTIAL_DB, target_values, "essential.results.csv")
    run_tests(PyDBLiteTest, config['iterations'], record_counts, all_functions, PYDBLITE_DB, target_values, 'pydb.results.csv')
    run_tests(TinyTest, config['iterations'], record_counts, all_functions, TINY_DB, target_values, "tiny.results.csv")


