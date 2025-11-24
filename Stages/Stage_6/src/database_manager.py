import pymssql
import configparser
import sys
from .data_loader import DataLoader
from .query_manager import QueryManager

class DatabaseManager:
    # CONSTANTS
    CONFIG_FILE = "config/auth.cfg"
    DATABASE_NAME = "nba_database_24_25"
    CREATE_TABLES_SCRIPT = "src/sql/create_tables.sql"
    CLEAR_DATABASE_SCRIPT = "src/sql/clear_database.sql"

    Q7_STAT_MAP = {
        "ppg" : "avgPoints",
        "apg" : "avgAssists",
        "spg" : "avgSteals"
    }

    def __init__(self):
        self._connect()
        self._data_loader = DataLoader(self._connection)
        self._query_manager = QueryManager(self._connection)
            
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
        self._data_loader.load_game()
        self._data_loader.load_play_in_game()
        self._data_loader.load_player_information()
        self._data_loader.load_draft_combine()
        self._data_loader.load_organization()
        self._data_loader.load_drafts()
        self._data_loader.create_team_wins_view()

    def populate_database(self):
        self._create_tables()
        self._load_database()

    def _parse_positive_int(self, input):
        try:
            n = int(input)
            if n <= 0:
                raise ValueError()
            return n
        
        except ValueError:
            print(f"Error: Expected a positive integer, but got '{input}'.")
            return None
        
    def _parse_winrate(self, input):
        try:
            num = float(input)
            if num < 0 or num > 1:
                raise ValueError()
            return num
            
        except ValueError:
            print(f"Error: Expected a number in the interval [0,1], but got '{input}'.")
            return None

    def run_s1(self, limit_str, page_str):
        limit = self._parse_positive_int(limit_str)
        page = self._parse_positive_int(page_str)
        if limit is not None and page is not None:
            return self._query_manager.get_s1(limit, page)
    
    def run_s2(self, limit_str, page_str):
        limit = self._parse_positive_int(limit_str)
        page = self._parse_positive_int(page_str)
        if limit is not None and page is not None:
            return self._query_manager.get_s2(limit, page)
    
    def run_s3(self):
        return self._query_manager.get_s3()
    
    def run_s4(self):
        return self._query_manager.get_s4()
    
    def run_s5(self):
        return self._query_manager.get_s5()
    
    def run_s6(self):
        return self._query_manager.get_s6()
    
    def run_s7(self, limit_str, page_str):
        limit = self._parse_positive_int(limit_str)
        page = self._parse_positive_int(page_str)
        if limit is not None and page is not None:
            return self._query_manager.get_s7(limit, page)

    def run_s8(self, limit_str, page_str):
        limit = self._parse_positive_int(limit_str)
        page = self._parse_positive_int(page_str)
        if limit is not None and page is not None:
            return self._query_manager.get_s8(limit, page)
    
    def run_q1(self, num_teams):
        n = self._parse_positive_int(num_teams)
        if n is not None:
            return self._query_manager.get_q1(n)
        
    def run_q2(self):
        return self._query_manager.get_q2()
    
    def run_q3(self, team_name, use_avg_str = None):
        parts = team_name.strip().split()
        name = ' '.join(parts)

        if use_avg_str == "--avg":
            use_avg = True
        elif use_avg_str is None:
            use_avg = False
        else:
            print(f"Error: Expected '--avg', but got '{use_avg_str}'.")
            return

        return self._query_manager.get_q3(name, use_avg)
    
    def run_q4(self, num_players_str, page_str):
        num_players = self._parse_positive_int(num_players_str)
        page = self._parse_positive_int(page_str)

        if num_players is not None and page is not None:
            return self._query_manager.get_q4(num_players, page)

    def run_q5(self):
        return self._query_manager.get_q5()
    
    def run_q6(self, team_name):
        parts = team_name.strip().split()
        name = ' '.join(parts)
        return self._query_manager.get_q6(name)
    
    def run_q7(self, stat_str, num_players_str):
        num_players = self._parse_positive_int(num_players_str)
        stat = self.Q7_STAT_MAP.get(stat_str)
        if stat is not None and num_players is not None:
            return self._query_manager.get_q7(stat, num_players)
        
        if stat is None:
            print(f"Error: Expected 'ppg', 'apg', or 'spg', but got '{stat_str}'.")

    def run_q8(self, team_name):
        parts = team_name.strip().split()
        name = ' '.join(parts)
        return self._query_manager.get_q8(name)
    
    def run_q9(self, game_id_str):
        game_id = self._parse_positive_int(game_id_str)
        if game_id is not None:
            return self._query_manager.get_q9(game_id)
        
    def run_q10(self, min_attempts_str, num_players_str):
        num_players = self._parse_positive_int(num_players_str)
        min_attempts = self._parse_positive_int(min_attempts_str)

        if num_players is not None and min_attempts is not None:
            return self._query_manager.get_q10(min_attempts, num_players)
        
    def run_q11(self, game_id_str):
        game_id = self._parse_positive_int(game_id_str)
        if game_id is not None:
            return self._query_manager.get_q11(game_id)
        
    def run_q12(self, home_name, away_name):
        parts_home = home_name.strip().split()
        parts_away = away_name.strip().split()
        home = ' '.join(parts_home)
        away = ' '.join(parts_away)
        return self._query_manager.get_q12(home, away)

    def run_q13(self, min_winrate_str):
        min_winrate = self._parse_winrate(min_winrate_str)
        if min_winrate is not None:
            return self._query_manager.get_q13(min_winrate)
        
    def run_q14(self, min_teams_str):
        min_teams = self._parse_positive_int(min_teams_str)
        if min_teams is not None:
            return self._query_manager.get_q14(min_teams)
        
        
        
        
        
