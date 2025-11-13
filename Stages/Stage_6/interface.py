from database import *
import textwrap

class Interface():
    SEP_BAR_LEN = 60
    EMOJI_LEN = 2
    RESET_COLOUR = "\033[0m"
    BRIGHT_ORANGE = "\033[38;5;214m"
    DARK_ORANGE = "\033[38;5;208m"
    BOLD_TEXT = "\033[1m"
    YELLOW = "\033[93m"
    BASKETBALL = "🏀"
    TAB = "   "

    def __init__(self):
        self._database = Database()
        self._print_welcome_message()
        self._print_help_menu()

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
        print("\n>")

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
            "s1" , "s2", "s3", "s4", "s5", "s6", "s7"
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
            "List all coaches along with their regular and playoff season stats",
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
        print("\n>")