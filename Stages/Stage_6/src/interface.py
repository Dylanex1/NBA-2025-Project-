from .database_manager import *
import textwrap
import os
import shlex

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

    CLEAR = "clear"
    EXIT = "exit"

    SIMPLE_CMDS = [
        "s1" , "s2", "s3", "s4", "s5", "s6", "s7", "s8"
    ]
    COMPLEX_CMDS = [
        "q1 <N>", "q2", "q3 \"<team_name>\" [--avg]", "q4 <limit> <page>", "q5",
        "q6 \"<team_name>\"", "q7 <stat> <N>", "q8 \"<team_name>\"", "q9 <game_id>",
        "q10 <min_attempts> <N>", "q11 <game_id>", "q12 \"<home_name>\" \"<away_name>\"",
        "q13 <min_winrate>", "q14"
    ]
    SYSTEM_CMDS = [
        "clear-db",
        "load",
        "clear",
        "exit"
    ]

    SIMPLE_DESCS = [
        "List all player draft combine stats",
        "List all player drafts",
        "List all coaches along with their regular season stats",
        "List all coaches along with their playoff season stats",
        "List all arenas",
        "List all teams",
        "List all games in the 2024-2025 season",
        "List all players along with personal information"
    ]
    COMPLEX_DESCS = [
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
    SYSTEM_DESCS = [
        "Clear the entire database (drop all tables)",
        "Clear and populate the database",
        "Clear the terminal screen",
        "Quit the program"
    ]

    def __init__(self):
        self._database_manager = DatabaseManager()
        self._print_welcome_message()

        self.CMDS = {
            "help" : {"argc" : 0, "run" : self._print_help_menu, "usage" : "help"},
            "clear" : {"argc" : 0, "run" : self._clear_screen, "usage" : "clear"},
            "clear-db" : {"argc" : 0, "run" : self._database_manager.clear_database, "usage" : "clear-db"},
            "load" : {"argc" : 0, "run" : self._database_manager.populate_database, "usage" : "load"},
            "exit" : {"argc" : 0, "run" : None, "usage" : "exit"},
            "s1" : {"argc" : 0, "run" : self._database_manager.run_s1, "usage" : "s1"},
            "s2" : {"argc" : 0, "run" : self._database_manager.run_s2, "usage" : "s2"},
            "s3" : {"argc" : 0, "run" : self._database_manager.run_s3, "usage" : "s3"},
            "s4" : {"argc" : 0, "run" : self._database_manager.run_s4, "usage" : "s4"},
            "s5" : {"argc" : 0, "run" : self._database_manager.run_s5, "usage" : "s5"},
            "s6" : {"argc" : 0, "run" : self._database_manager.run_s6, "usage" : "s6"},
            "s7" : {"argc" : 0, "run" : self._database_manager.run_s7, "usage" : "s7"},
            "s8" : {"argc" : 0, "run" : self._database_manager.run_s8, "usage" : "s8"},
            "q1" : {"argc" : 1, "run" : self._database_manager.run_q1, "usage" : "q1 <N>"},
            "q2" : {"argc" : 0, "run" : self._database_manager.run_q2, "usage" : "q2"},
            "q3" : {"argc" : (1, 2), "run" : self._database_manager.run_q3, "usage" : "q3 \"<team_name>\" [--avg]"},
            "q4" : {"argc" : 2, "run" : self._database_manager.run_q4, "usage" : "q4 <limit> <page>"},
            "q5" : {"argc" : 0, "run" : self._database_manager.run_q5, "usage" : "q5"},
            "q6" : {"argc" : 1, "run" : self._database_manager.run_q6, "usage" : "q6 \"<team_name>\""},
            "q7" : {"argc" : 2, "run" : self._database_manager.run_q7, "usage" : "q7 <stat> <N>"},
            "q8" : {"argc" : 1, "run" : self._database_manager.run_q8, "usage" : "q8 \"<team_name>\""},
            "q9" : {"argc" : 1, "run" : self._database_manager.run_q9, "usage" : "q9 <game_id>"},
            "q10" : {"argc" : 2, "run" : self._database_manager.run_q10, "usage" : "q10 <min_attempts> <N>"},
        }

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

    def _get_cmd_width(self):
        max_l1 = max(len(s) for s in self.SIMPLE_CMDS)
        max_l2 = max(len(s) for s in self.COMPLEX_CMDS)
        max_l3 = max(len(s) for s in self.SYSTEM_CMDS)
        return max(max_l1, max_l2, max_l3) + len(self.TAB)
    
    def _print_cmds(self, header, cmds, descs, cmd_width):
        print("\n" + self._colour_string(self.BRIGHT_ORANGE, header, True))
        for (cmd, desc) in zip(cmds, descs):
            print(self.TAB + self._colour_string(self.YELLOW, f"{cmd:<{cmd_width}}") + desc)

    def _print_help_menu(self):
        title = " HELP MENU - NBA DATABASE "

        cmd_width = self._get_cmd_width()
        print()
        self._print_centered_title(title)
        self._print_cmds("Simple Queries:", self.SIMPLE_CMDS, self.SIMPLE_DESCS, cmd_width)
        self._print_cmds("Complex Queries:", self.COMPLEX_CMDS, self.COMPLEX_DESCS, cmd_width)
        self._print_cmds("System:", self.SYSTEM_CMDS, self.SYSTEM_DESCS, cmd_width)
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
    
    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _print_arg_error(self, cmd, num_args_given):
        argc = self.CMDS[cmd]["argc"]
        usage = self.CMDS[cmd]["usage"]

        min_argc = argc

        if isinstance(argc, int):
            min_argc = argc
        else:
            min_argc = min(argc)

        if num_args_given < min_argc:
            print(f"Too few arguments for '{cmd}'.")
        else:
            print(f"Too many arguments for '{cmd}'.")

        print(f"Usage: {usage}.")

    def run(self):
        done = False
        just_cleared = False
        while not done:
            prompt = "nba-db> " if just_cleared else "\nnba-db> "
            user_input = input(prompt)
            done, just_cleared = self._process_user_input(user_input)
                
    def _process_user_input(self, input):
        try:
            parts = shlex.split(input.strip().lower())
            if not parts or parts[0] not in self.CMDS:
                raise ValueError()
            return self._process_cmd(parts)
        
        except ValueError:
            print("Invalid command.")
            return False, False
    
    def _process_cmd(self, input):
        done = False
        just_cleared = False
        cmd = input[0]
        args = input[1:]
        num_args_given = len(args)

        argc = self.CMDS[cmd]["argc"]
        cond1 = isinstance(argc, int) and argc != num_args_given
        cond2 = isinstance(argc, tuple) and num_args_given not in argc
        if cond1 or cond2:
            self._print_arg_error(cmd, num_args_given)
            return done, just_cleared

        if cmd == self.CLEAR:
            just_cleared = True
        elif cmd == self.EXIT:
            done = True

        if self.CMDS[cmd]["run"] is not None:
            results = self.CMDS[cmd]["run"](*args)

            if results is not None:
                self._print_table(results) 

        return done, just_cleared
        


            




