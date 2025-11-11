import pandas as pd

class DataLoader:
    # CONSTANTS
    ARENA_CSV = "Datasets/Arena.csv"
    COACH_CSV = "Datasets/Coach.csv"
    DRAFT_COMBINE_CSV = "Datasets/DraftCombine.csv"
    DRAFTS_CSV = "Datasets/Drafts.csv"
    GAME_CSV = "Datasets/Game.csv"
    ORGANIZATION_CSV = "Datasets/Organization.csv"
    PLAYER_CSV = "Datasets/Player.csv"
    PLAYER_INFORMATION_CSV = "Datasets/PlayerInformation.csv"
    PLAY_IN_GAME_CSV = "Datasets/PlayInGame.csv"
    PLAYOFF_COACH_STATS_CSV = "Datasets/PlayoffGameCoachStats.csv"
    REGULAR_COACH_STATS_CSV = "Datasets/RegularGameCoachStats.csv"
    TEAM_CSV = "Datasets/Team.csv"

    def __init__(self, connection):
        self._connection = connection

    def _check_null(self, val):
        return None if pd.isna(val) else val

    def load_arena(self):
        df = pd.read_csv(self.ARENA_CSV)
        sql = """
            INSERT INTO Arena (
                ArenaName, 
                SeatingCapacity, 
                OpeningYear, 
                ArenaCityName
            )
            VALUES (%s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            for row in df.itertuples(index=False):

                params = (
                    row.ArenaName,
                    self._check_null(row.SeatingCapacity),
                    self._check_null(row.OpeningYear),
                    self._check_null(row.ArenaCityName)
                )

                cursor.execute(sql, params)
            self._connection.commit()

    def load_team(self):
        df = pd.read_csv(self.TEAM_CSV)
        sql = """
            INSERT INTO Team (
                TeamID, 
                TeamName,
                TeamAbbrv,
                Nickname,
                [State],
                YearFounded,
                ArenaName
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            for row in df.itertuples(index=False):

                params = (
                    row.TeamID,
                    self._check_null(row.TeamName),
                    self._check_null(row.TeamAbbrv),
                    self._check_null(row.Nickname),
                    self._check_null(row.State),
                    self._check_null(row.YearFounded),
                    self._check_null(row.ArenaName)
                )

                cursor.execute(sql, params)
            self._connection.commit()
        
    def load_coach(self):
        df = pd.read_csv(self.COACH_CSV)
        sql = """
            INSERT INTO Coach (
                CoachID,
                CoachName,
                TeamID,
                SeasonsFranchise,
                SeasonsOverall
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            for row in df.itertuples(index=False):

                params = (
                    row.CoachID,
                    self._check_null(row.CoachName),
                    self._check_null(row.TeamID),
                    self._check_null(row.SeasonsFranchise),
                    self._check_null(row.SeasonsOverall)
                )

                cursor.execute(sql, params)
            self._connection.commit()

    def load_playoff_coach_stats(self):
        df = pd.read_csv(self.PLAYOFF_COACH_STATS_CSV)
        sql = """
            INSERT INTO PlayoffGameCoachStats (
                CoachID,
                PlayoffsCurrentG,
                PlayoffsCurrentW,
                PlayoffsCurrentL,
                PlayoffsFranchiseG,
                PlayoffsFranchiseW,
                PlayoffsFranchiseL,
                PlayoffsOverallG,
                PlayoffsOverallW,
                PlayoffsOverallL
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            for row in df.itertuples(index=False):

                params = (
                    row.CoachID,
                    self._check_null(row.Playoffs_Current_G),
                    self._check_null(row.Playoffs_Current_W),
                    self._check_null(row.Playoffs_Current_L),
                    self._check_null(row.Playoffs_Franchise_G),
                    self._check_null(row.Playoffs_Franchise_W),
                    self._check_null(row.Playoffs_Franchise_L),
                    self._check_null(row.Playoffs_Overall_G),
                    self._check_null(row.Playoffs_Overall_W),
                    self._check_null(row.Playoffs_Overall_L)
                )

                cursor.execute(sql, params)
            self._connection.commit()

    def load_regular_coach_stats(self):
        df = pd.read_csv(self.REGULAR_COACH_STATS_CSV)
        sql = """
            INSERT INTO RegularGameCoachStats (
                CoachID,
                RegCurrentG,
                RegCurrentW,
                RegCurrentL,
                RegFranchiseG,
                RegFranchiseW,
                RegFranchiseL,
                RegOverallG,
                RegOverallW,
                RegOverallL
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        with self._connection.cursor() as cursor:
            for row in df.itertuples(index=False):

                params = (
                    row.CoachID,
                    self._check_null(row.Reg_Current_G),
                    self._check_null(row.Reg_Current_W),
                    self._check_null(row.Reg_Current_L),
                    self._check_null(row.Reg_Franchise_G),
                    self._check_null(row.Reg_Franchise_W),
                    self._check_null(row.Reg_Franchise_L),
                    self._check_null(row.Reg_Overall_G),
                    self._check_null(row.Reg_Overall_W),
                    self._check_null(row.Reg_Overall_L)
                )

                cursor.execute(sql, params)
            self._connection.commit()

    def load_player(self):
        df = pd.read_csv(self.PLAYER_CSV)
        team_df = pd.read_csv(self.TEAM_CSV)
        team_csv_ids = set(team_df.TeamID)
        sql = """
            INSERT INTO Player (
                PlayerID,
                FirstName,
                LastName,
                TeamID
            )
            VALUES (%s, %s, %s, %s)
        """

        params_list = []
        for row in df.itertuples(index=False):

            if pd.isna(row.TeamID):
                teamID = None
            else:
                tid = int(row.TeamID)
                teamID = tid if tid in team_csv_ids else None

            params_list.append(
                (
                    row.PlayerID,
                    self._check_null(row.FirstName),
                    self._check_null(row.LastName),
                    teamID
                )
            )

        with self._connection.cursor() as cursor:
            cursor.executemany(sql, params_list)
            self._connection.commit()

    def load_game(self):
        df = pd.read_csv(self.GAME_CSV)

        df["Date"] = pd.to_datetime(
            df["Date"].str.strip(),
            format = "%a, %b %d, %Y"
        ).dt.date

        rename_map = {
            "FedEx Forum": "FedExForum",
            "Rocket Arena": "Rocket Mortgage Fieldhouse",
            "Madison Square Garden ": "Madison Square Garden",

        }

        null_arenas = {
            "Intuit Dome",
            "Mexico City Arena",
            "T-Mobile Arena",
            "AccorHotels Arena",
            "Moody Center"
        }

        df["Arena"] = df["Arena"].str.strip()
        df["Length"] = df["Length"].str.strip()
        df["Length"] = df["Length"].replace("N", None)
        df["Arena"] = df["Arena"].replace(rename_map)
        df.loc[df["Arena"].isin(null_arenas), "Arena"] = None


        sql = """
            INSERT INTO Game (
                GameID,
                [Date],
                HomePTS,
                VisitorPTS,
                [Length],
                Arena,
                Overtime,
                AttendingAmount,
                HomeTeamID,
                VisitorTeamID
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params_list = []
        for row in df.itertuples(index=False):
            params_list.append(
                (
                    row.GameID,
                    row.Date,
                    self._check_null(row.HomePTS),
                    self._check_null(row.VisitorPTS),
                    self._check_null(row.Length),
                    self._check_null(row.Arena),
                    self._check_null(row.Overtime),
                    self._check_null(row.AttendingAmount),
                    row.HomeTeamID,
                    row.VisitorTeamID
                )
            )

        with self._connection.cursor() as cursor:
            cursor.executemany(sql, params_list)
            self._connection.commit()