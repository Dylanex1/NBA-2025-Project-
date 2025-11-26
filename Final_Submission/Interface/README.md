## Instructions

### Step 1

This program uses `pandas` to load the CSV files into Python and also preprocesses the data. It also uses `pymssql` as the API to connect to `uranium`.

To install both `pandas` and `pymssql`, type `make` in the command line. Once those two modules are installed, the program can be run with `make run`. The order of commands is:

1) `make`
2) `make run`

### Step 2

The database will initially be populated when running the program for the first time. If you do not want to clear or populate the database yet, you can skip this step for now. The help menu shows the commands for clearing and populating the database.

- `clear-db` is the command used to clear all rows and tables from the database.
- `load` is the command used to create all tables in the database and then populate them. This command also calls `clear-db` before loading to ensure fresh data enters the system.

## Notes

You will not have to worry about authentication, as the `username` and `password` are stored in the `auth.cfg` file in the `config` directory. This file is read by `database_manager.py`, which manages the connection to `uranium`. However, in case you need the credentials, they are below:

- username = beyakd1
- password = 7974864

In the main directory, there is a folder titled `extra` that is not used when running the interface. This folder contains another folder called `data_processing`, which includes the Python scripts that were used to normalize the dataset. These scripts are only included as additional context for grading and are not required to run the program.
