config = {

    # whre to store and read generated mock data
    'mock_directory': "mock-data",

    # where the db files should be written to
    'db_directory': "dbfiles",

    # how many records in each test
    'record_counts': range(10000, 110000, 10000),
    # how many iterations to run each function - will be averaged in output
    'iterations': 10,

    # for selections
    # shouldn't need to change these unless you change the data model
    'target_values': {
        "get_one": "a-very-unique-slug",
        "get_nested": "targetuser@example.com",
        "update_one": "another-very-unique-slug",
        "delete_one": "third-very-unique-slug",
    }

}
