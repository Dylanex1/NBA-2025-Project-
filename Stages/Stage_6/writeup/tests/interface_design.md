---
output:
  pdf_document: default
---

## Interface Design

Our project uses a command-line interface (CLI) with an orange basketball-themed colour scheme, since we're working with NBA data. When the program is run, the user is greeted with a welcome message that briefly describes the database and what information is available to them. The welcome message instructs the user to type `help` to see a list of available commands. All query results are printed using dynamically sized columns with orange headers that are underlined for readability. 

The help menu is divided into three sections. The first section lists the simple queries, which display entire tables. These simple queries are used as reference tools for getting the input needed for complex queries. For example, if a complex query requires a GameID, the user should run the game table query to find the GameID of interest, then use that value as input for the complex query. The second section lists the complex queries. Finally, the third section lists system-level commands like clearing or repopulating the database, clearing the screen, or exiting the program. Each command in the help menu includes the command the user must enter, along with any parameters, and a short description of what the command does.

The interface is implemented in Python. We created a `DatabaseManager` class, which serves as the central manager for all database operations. It manages the connection by reading the configuration file and runs SQL scripts to create tables and views, as well as clear the entire database. It also orchestrates data loading and querying through its `DataLoader` and `QueryManager` instance variables. The `DataLoader` loads and validates all CSV files into Python using `pandas`, then inserts the data into the SQL Server using prepared statements through `pymssql`. The `QueryManager` class handles all queries sent to SQL Server, again using prepared statements to prevent SQL injection. Finally, we created an `Interface` class that handles user interaction. It displays the welcome message, help menu, and neatly formatted query results. Additionally, it parses user input and sends commands to the `DatabaseManager`.

## Diagrams

This section shows diagrams illustrating how the interface will look.

![Welcome Message Screenshot](welcome.png)

![Help Menu Screenshot](help.png)

![Query Results Screenshot](query.png)


### Prevention of SQL injection
The plan of how our interface will prevent users from being malicious is first off our interface will only accept a small set of commands to run and those commands will be given to the user and they can search or do actions only with those certain commands if one of the commands is not entered then give a message to the user saying use one of the following commands. This already prevents a good amount of malformed CLI interfaces that may allow a user to input anything and potentially harm the database or crash it. Next when they run any of the set of commands we will use prepared statements and ? in the string query for user input which will limit any SQL injection into the database querys/manipulation since prepared statemtents will take any user input as VALUES. As an additonal layer of security we can grab the user input before the query is executed and look for any keywords that a user should not be able to run. For example if a user inputs SELECT,DELETE,WHERE,OR,AND,=,--,',UPDATE,ALTER and so on we can give an error message for the user saying that is not a valid input please try again. With this plan in place there should be no way for malicious activity.
