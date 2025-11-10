import pymssql
import configparser
import sys
from dataLoader import DataLoader

class Database:
    # CONSTANTS
    CONFIG_FILE = "auth.cfg"
    DATABASE_NAME = "nba_database_24_25"
    CREATE_TABLES_SCRIPT = "create_tables.sql"
    CLEAR_DATABASE_SCRIPT = "clear_database.sql"

    def __init__(self):
        self._connect()
        self._data_loader = DataLoader(self._connection)
            
    def _connect(self):
        config_items = self._get_config_items()

        try:
            self._connection = pymssql.connect(
                server=config_items["server"],
                user=config_items["username"],
                password=config_items["password"],
                database=config_items["database"]
            )

        except pymssql.Error as e:
            print("Database _connection failed.")
            print(f"Details: {e}") 
            sys.exit(1)

    def _get_config_items(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.CONFIG_FILE)
            db_config = config[self.DATABASE_NAME]

            config_items = {
                "server" : db_config.get("server"),
                "username" : db_config.get("username"),
                "password" : db_config.get("password"),
                "database" : db_config.get("database")
            }

            self._print_config_errors(config_items)
            return config_items

        except FileNotFoundError as fnfe:
            print(f"Unable to find {self.CONFIG_FILE}.")
            sys.exit(1)

        except configparser.Error as ce:
            print(f"Error parsing {self.CONFIG_FILE}.")
            sys.exit(1)

    def _print_config_errors(self, config_items):
        missing_items = [item for item in config_items if config_items[item] is None]
        if len(missing_items) > 0:
            print(f"Missing config items: {", ".join(missing_items)}")
            sys.exit(1)

    def clear_database(self):
        try:
            with open(self.CLEAR_DATABASE_SCRIPT, "r") as clear_script:
                script = clear_script.read()

            with self._connection.cursor() as cursor:
                cursor.execute(script)
                self._connection.commit()

        except FileNotFoundError as fnfe:
            print(f"Unable to find {self.CLEAR_DATABASE_SCRIPT}.")
            sys.exit(1)

        except pymssql.Error as e:
            print(f"Error executing {self.CLEAR_DATABASE_SCRIPT}.")
            print(f"Details: {e}")
            sys.exit(1)

        except OSError as ose:
            print(f"Error parsing {self.CLEAR_DATABASE_SCRIPT}.")
            sys.exit(1)

    def _create_tables(self):
        self.clear_database()

        try:
            with open(self.CREATE_TABLES_SCRIPT, "r") as create_tables_script:
                script = create_tables_script.read()

            with self._connection.cursor() as cursor:
                cursor.execute(script)
                self._connection.commit()

        except FileNotFoundError as fnfe:
            print(f"Unable to find {self.CREATE_TABLES_SCRIPT}.")
            sys.exit(1)

        except pymssql.Error as e:
            print(f"Error executing {self.CREATE_TABLES_SCRIPT}.")
            print(f"Details: {e}")
            sys.exit(1)

        except OSError as ose:
            print(f"Error parsing {self.CREATE_TABLES_SCRIPT}.")
            sys.exit(1)

    def _load_database(self):
        self._data_loader.load_arena()
        self._data_loader.load_team()
        self._data_loader.load_coach()
        self._data_loader.load_playoff_coach_stats()
        self._data_loader.load_regular_coach_stats()
        self._data_loader.load_player()

    def populate_database(self):
        self._create_tables()
        self._load_database()
