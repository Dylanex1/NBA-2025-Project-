from .database_manager import *
import textwrap
import os

class Interface:
    # Constants
    RESET_COLOUR = "\033[0m"
    BRIGHT_ORANGE = "\033[38;5;214m"
    DARK_ORANGE = "\033[38;5;208m"
    BOLD_TEXT = "\033[1m"
    YELLOW = "\033[93m"

    SEP_BAR_LEN = 60
    EMOJI_LEN = 2
    BASKETBALL = "🏀"
    TAB = "   "

    HELP = "help"
    CLEAR = "clear"
    CLEAR_DB = "clear_db"
    LOAD = "load"
    EXIT = "exit"

    S1 = "s1"
    S2 = "s2"
    S3 = "s3"
    S4 = "s4"
    S5 = "s5"
    S6 = "s6"
    S7 = "s7"
    S8 = "s8"

    def __init__(self):
        self._database_manager = DatabaseManager()
        self._print_welcome_message()

    def _colour_string(self, colour, string, bold = False):
        if bold:
            return f"{colour}{self.BOLD_TEXT}{string}{self.RESET_COLOUR}"
        
        return f"{colour}{string}{self.RESET_COLOUR}"
    
    def _get_center_spacing(self, length, string):
        str_len = len(string)
        num_spaces = length - str_len
        left_space = num_spaces // 2 
        right_space = num_spaces - left_space
        return left_space, right_space
    
    def _print_centered_title(self, title):
        title_formatted = (
            self.BASKETBALL 
            + self._colour_string(self.BRIGHT_ORANGE, title, True)
            + self.BASKETBALL 
        ) 

        left_space, right_space = self._get_center_spacing(self.SEP_BAR_LEN - 2*self.EMOJI_LEN, title)
        print(self._colour_string(self.DARK_ORANGE, "=" * self.SEP_BAR_LEN))
        print((" " * left_space) + title_formatted + (" " * right_space))
        print(self._colour_string(self.DARK_ORANGE, "=" * self.SEP_BAR_LEN))
    
    def _print_welcome_message(self):
        title = " NBA 2024-2025 SEASON DATABASE "
        welcome_paragraph = (
            "Welcome to the 2024-2025 NBA Season Database. This interface "
            "allows you to explore teams, players, game, coaches, draft stats, and more."
        )         
        help_message = (
            "Type \'"
            + self._colour_string(self.YELLOW, "help")
            + "\' to see a list of available commands."
        )

        self._print_centered_title(title)
        print("\n" + textwrap.fill(welcome_paragraph, self.SEP_BAR_LEN))
        print("\n" + help_message)
        print(self._colour_string(self.DARK_ORANGE, "-" * self.SEP_BAR_LEN))

    def _get_cmd_width(self, l1, l2, l3):
        max_l1 = max(len(s) for s in l1)
        max_l2 = max(len(s) for s in l2)
        max_l3 = max(len(s) for s in l3)
        return max(max_l1, max_l2, max_l3) + len(self.TAB)
    
    def _print_cmds(self, header, cmds, descs, cmd_width):
        print("\n" + self._colour_string(self.BRIGHT_ORANGE, header, True))
        for (cmd, desc) in zip(cmds, descs):
            print(self.TAB + self._colour_string(self.YELLOW, f"{cmd:<{cmd_width}}") + desc)

    def _print_help_menu(self):
        title = " HELP MENU - NBA DATABASE "

        simple_query_cmds = [
            "s1" , "s2", "s3", "s4", "s5", "s6", "s7", "s8"
        ]
        complex_query_cmds = [
            "q1 <N>", "q2", "q3 <team_name> [--avg]", "q4 <limit> <page>", "q5",
            "q6 <team_name>", "q7 <stat> <N>", "q8 <team_name>", "q9 <game_id>",
            "q10 <min_attempts> <N>", "q11 <game_id>", "q12 <home_name> <away_name>",
            "q13 <min_winrate>", "q14"
        ]
        system_cmds = [
            "clear-db",
            "load",
            "clear",
            "exit"
        ]

        simple_query_descs = [
            "List all player draft combine stats",
            "List all player drafts",
            "List all coaches along with their regular season stats",
            "List all coaches along with their playoff season stats",
            "List all arenas",
            "List all teams",
            "List all games in the 2024-2025 season",
            "List all players along with personal information"
        ]
        complex_query_descs = [
            "Show the top N teams by wins along with their season averages",
            "Show coaches with 5+ seasons and a positive playoff win rate",
            "Shows a team's average PPG (optionally include league average)",
            "List <limit> players from <page> by position/height with PPG/APG/SPG",
            "Show the team and coach that won the 2024-2025 championship",
            "Show a team's roster ordered by PPG, APG, and SPG",
            "Show the top N players ordered by a chosen stat (PPG, APG, SPG)",
            "Show the average age of players on a team",
            "Show both teams' stats for a specific game",
            "Show the top N players ordered by 3P% with a minimum attempt requirement",
            "Show centers that are 6\"5+ and their points in a specific game",
            "Show a home team's win percentage against a specific visiting team",
            "Show coaches with a playoff winrate ≥ a decimal input (ex. 0.75)",
            "Show arenas where every team has won at least once"
        ]
        system_descs = [
            "Clear the entire database (drop all tables)",
            "Clear and populate the database",
            "Clear the terminal screen",
            "Quit the program"
        ]

        cmd_width = self._get_cmd_width(simple_query_cmds, complex_query_cmds, system_cmds)
        print()
        self._print_centered_title(title)
        self._print_cmds("Simple Queries:", simple_query_cmds, simple_query_descs, cmd_width)
        self._print_cmds("Complex Queries:", complex_query_cmds, complex_query_descs, cmd_width)
        self._print_cmds("System:", system_cmds, system_descs, cmd_width)
        print(self._colour_string(self.DARK_ORANGE, "-" * self.SEP_BAR_LEN))

    def _get_col_widths(self, cols, rows):
        widths = []
        for col in cols:
            widths.append(len(col))

        for row in rows:
            for i, col in enumerate(cols):
                val = row[col]
                val_str = "NULL" if val is None else str(val).strip() 
                width = len(val_str)
                if width > widths[i]:
                    widths[i] = width

        return widths
    
    def _print_col_headers(self, cols, widths):
        headers = ["\n"]
        for i, col in enumerate(cols):
            col_padded = f"{col:<{widths[i]}}"
            headers.append(self._colour_string(self.BRIGHT_ORANGE, col_padded, True)  + self.TAB)
        
        print("".join(headers))
    
    def _print_header_underlines(self, widths):
        underlines = []
        for width in widths:
            underlines.append(self._colour_string(self.DARK_ORANGE, "-" * width) + self.TAB)
        
        print("".join(underlines))

    def _print_rows(self, widths, rows, cols):
        for row in rows:
            row_strs = []
            for i, col in enumerate(cols):
                val = row[col]
                val_str = "NULL" if val is None else str(val).strip() 
                row_strs.append(f"{val_str:<{widths[i]}}" + self.TAB)

            print("".join(row_strs))

    def _print_table(self, rows):
        if not rows:
            print("No results.")
            return
    
        cols = list(rows[0].keys())
        widths = self._get_col_widths(cols, rows)
        self._print_col_headers(cols, widths)
        self._print_header_underlines(widths)
        self._print_rows(widths, rows, cols)

    def run(self):
        done = False
        just_cleared = False
        while not done:
            prompt = "> " if just_cleared else "\n> "
            user_input = input(prompt).strip().lower().split()
            just_cleared = False

            if len(user_input) == 1 and user_input[0] == self.HELP:
                self._print_help_menu()

            elif len(user_input) == 1 and user_input[0] == self.CLEAR:   
                os.system('cls' if os.name == 'nt' else 'clear')
                just_cleared = True

            elif len(user_input) == 1 and user_input[0] == self.CLEAR_DB:
                self._database_manager.clear_database()

            elif len(user_input) == 1 and user_input[0] == self.LOAD:
                self._database_manager.populate_database()

            elif len(user_input) == 1 and user_input[0] == self.EXIT:
                done = True

            elif len(user_input) == 1 and user_input[0] == self.S1:
                self._print_table(self._database_manager.run_s1())

            elif len(user_input) == 1 and user_input[0] == self.S2:
                self._print_table(self._database_manager.run_s2())

            elif len(user_input) == 1 and user_input[0] == self.S3:
                self._print_table(self._database_manager.run_s3())

            elif len(user_input) == 1 and user_input[0] == self.S4:
                self._print_table(self._database_manager.run_s4())

            elif len(user_input) == 1 and user_input[0] == self.S5:
                self._print_table(self._database_manager.run_s5())

            elif len(user_input) == 1 and user_input[0] == self.S6:
                self._print_table(self._database_manager.run_s6())

            elif len(user_input) == 1 and user_input[0] == self.S7:
                self._print_table(self._database_manager.run_s7())

            elif len(user_input) == 1 and user_input[0] == self.S8:
                self._print_table(self._database_manager.run_s8())

