# python-db-performance
Performance benchmarking for a set of pure python databases

## Step 1: Generate mock data

Generate mock data for the tests by running `generate_mock_data.py`

## Step 2: Run the tests

Run the tests by running `test_db.py`

## Step 3: Review results

They will be in csv files with names corresponding to the database.

## Step 4: Clean up before you run again!

This is important: clean out the dbfiles directory or the databases 
will just keep growing and the times will be way off (doubling each time actually)

