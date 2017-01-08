## Python Database Performance Benchmarks

Performance benchmarking for a set of pure python databases, currently supporting:

- [TinyDB](https://github.com/msiemens/tinydb)
- [PyDbLite](https://github.com/PierreQuentel/PyDbLite)
- [EssentialDB](https://github.com/shane-mason/essentialdb)

### Disclosure:

I am the primary author of EssentialDB, so I have an inherent bias but tried to make these tests as non-biased as possible.

If you have any suggestions on how to optimize any of the queries for any of the databases, please let me know.

### The Data

The first requirement here is that tests could be replicated - this required consistent data. For this, we generated all the data up front. The documents are based on the following example:

    {
        "permissions":{
            "owner": "randomuser@example.com",
            "contributors": ["rand1@example.com", "rand2@example.com" ...]
        },
        "slug": "a_unique_string",
        "created": 1470455125.213304,
        "due": 1474083925.213304,
        "priority": "minor",
        "status": "started",
        "projects": ["project1", "project2" ... ],
        "labels": ["python", "database" ... ],
        "title": "Test Python Databases",
        "details": "Test several python databases head to head."
     }
     
I created a script to generate random data and save it to disk as plain old python objects (dictionaries really) using shelve. This way, the data can be read into the different databases so that results are constant. The script generates each data entry using the following rules:

- permissions - Complex object
- permissions.owner - Random fake email address from users list
- permissions.contributers - Array of 0 to 3 fake email addresses from users list
- slug - A unique string based on the project name and incrementing counts
- created - Integer epoch timestamp of creation (1 to 500 days in the past)
- due - Integer epoch timestamp the task is due (0 to 30 days after created timestamp)
- priority - randomly selected from [none, minor, major, critical, blocker]
- status - randomly selected from [none, started, blocked, closed, completed]
- projects - Array of 1 to 4 words, randomly selected from a list of generated project ‘names’
- labels - Array of 0 to 3 labels, randomly selected from a list of generated labels
- title - String 4 to 12 random lorem ipsum words
- description - String of 1 and 10 random lorem ipsum paragraphs

The script begins with 10k records and then adds 10k records until it reaches 100k, saving each iteration to disk [100k, 200k, 300k ... 1000k]. To model growth you might see in a real system, for each 100 k records added, the script generates 1000 additional users, project names and labels to be randomly selected when generating new entries. After the new entries are added to the dataset, the script shuffles before writing to disk.

With 10 files ranging from 10K to 100K - modeling snapshots of a growing database - we are ready to start looking at the tests.

### The Tests

The job of `test_db`` is to run through each of the previously stored datasets. Basically, it operates list this

    For dataset in [10k, 20k ... 100k]
        populate database For each function
    
    For each iteration
        initialize database object 
        start timer 
        run function 
        stop timer
    average = time/iterations

The tests do not take advantage of indexing speedups, though indexing is supported in each. 

### Functions

- insert_multiple - Adds a list of documents into the database
- get_one - Queries for one document by slug
- get_many - Query for all documents where priority == minor
- get_complex_and - Query for all documents where priority == blocker AND status == blocked
- get_complex_or - Query for all documents where status == closed OR priority == critical
- get_nested - Query for all documents where permissions.owner == prechosen name
- update_one - Update one document to have status = completed
- update_many - Update all where priority == minor to have status = closed
- delete_one - Delete one document by slug
- delete_many - Delete all documents where status == none

## Try It Yourself


## Step 0: Setup

Download

    git clone https://github.com/shane-mason/python-db-performance.git

Install or update the databases

    pip3 install --upgrade tinydb
    pip3 install --upgrade pydblite
    pip3 install --upgrade essentialdb

Make the data dirs

    mkdir mock-data
    mkdir dbfiles
    
Edit the configuration in `test_config.py`

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
    
    }`
    
### Step 1: Generate mock data

Generate mock data for the tests by running `generate_mock_data.py` This will create
a set of files in the mock-data directory.

### Step 2: Run the tests

Run the tests by running `test_db.py`

### Step 3: Review results

They will be in csv files with names corresponding to the database.

### Step 4: Clean up before you run again!

This is important: clean out the dbfiles directory or the databases 
will just keep growing and the times will be way off (doubling each time actually)

