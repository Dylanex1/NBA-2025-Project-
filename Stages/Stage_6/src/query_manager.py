class QueryManager:
    def __init__(self, connection):
        self._connection = connection

    def get_s1(self, limit, page):
        offset = (page - 1) * limit
        sql = """
            SELECT * 
            FROM DraftCombine
            ORDER BY PlayerID
            OFFSET %s ROWS
            FETCH NEXT %s ROWS ONLY;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (offset, limit))
            rows = cursor.fetchall()

        return rows

    def get_s2(self, limit, page):
        offset = (page - 1) * limit
        sql = """
            SELECT * 
            FROM Drafts
            ORDER BY Season
            OFFSET %s ROWS
            FETCH NEXT %s ROWS ONLY;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (offset, limit))
            rows = cursor.fetchall()

        return rows

    def get_s3(self):
        sql = """
            SELECT *
            FROM Coach AS C
            JOIN RegularGameCoachStats RGCS
            ON C.CoachID= RGCS.CoachID;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_s4(self):
        sql = """
            SELECT *
            FROM Coach AS C
            JOIN PlayoffGameCoachStats PGCS
            ON C.CoachID = PGCS.CoachID;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_s5(self):
        sql = """
            SELECT * 
            FROM Arena
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_s6(self):
        sql = """
            SELECT * 
            FROM Team;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_s7(self, limit, page):
        offset = (page - 1) * limit
        sql = """
            SELECT * 
            FROM Game
            ORDER BY GameID
            OFFSET %s ROWS
            FETCH NEXT %s ROWS ONLY;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (offset, limit))
            rows = cursor.fetchall()

        return rows

    def get_s8(self, limit, page):
        offset = (page - 1) * limit
        sql = """
            SELECT 
                Player.*,
                Birthdate,
                School,
                Country,
                [Weight],
                SeasonsPlayed,
                Position,
                FromYear,
                ToYear,
                Height,
                IsActive
            FROM Player
            LEFT JOIN PlayerInformation
            ON Player.PlayerID = PlayerInformation.PlayerID
            ORDER BY PlayerID
            OFFSET %s ROWS
            FETCH NEXT %s ROWS ONLY;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (offset, limit))
            rows = cursor.fetchall()

        return rows

    def _query_team_wins(self):
        return """
            SELECT
                t.TeamID,
                t.TeamName,
                RGCS.RegCurrentW AS Wins
            FROM RegularGameCoachStats RGCS
            JOIN Coach c ON RGCS.CoachID= c.CoachID
            JOIN Team t ON c.TeamID= t.TeamID
        """

    def _query_player_stats(self):
        return """
            SELECT
                p.PlayerID,
                p.TeamID,
                p.FirstName,
                p.LastName,
                COUNT(pIN.GameID) AS games_played,
                ROUND(
                    AVG(
                        (pIN.FG - pIN.[3P])*2 + pIN.[3P]*3 + pIN.FT
                    ),1
                ) AS avgPoints,
                ROUND(AVG(pIN.AST),1) AS avgAssists,
                ROUND(AVG(pIN.STL),1) AS avgSteals,
                ROUND(AVG(pIN.MP),1) AS avgMinutesPlayed,
                ROUND(AVG(pIN.FG), 1) AS avgFieldGoalsMade,
                ROUND(AVG(pIN.FGA), 1) AS avgFieldGoalsAttempted,
                ROUND(AVG(pIN.[3P]), 1) AS avgThreePointersMade,
                ROUND(AVG(pIN.[3PA]), 1) AS avgThreePointersAttempted,
                ROUND(AVG(pIN.FT), 1) AS avgFreeThrowsMade,
                ROUND(AVG(pIN.FTA), 1) AS avgFreeThrowsAttempted,
                ROUND(CAST(SUM(pIN.FG) AS FLOAT) / NULLIF(SUM(pIN.FGA), 0), 3) AS fieldGoalPct,
                ROUND(CAST(SUM(pIN.[3P]) AS FLOAT) / NULLIF(SUM(pIN.[3PA]), 0), 3) AS threePointPct,
                ROUND(CAST(SUM(pIN.FT) AS FLOAT)/ NULLIF(SUM(pIN.FTA), 0), 3) AS freeThrowPct
            From Player p
            JOIN PlayInGame pIN ON p.PlayerID= pIN.PlayerID
            GROUP BY p.PlayerID, p.FirstName,p.LastName, p.TeamID
        """

    def _query_team_stats(self):
        return """
            SELECT
                TW.Wins,
                TW.TeamName,
                TW.TeamID,
                ROUND(AVG(pS.avgPoints),1) AS avgTeamPoints,
                ROUND(AVG(pS.avgAssists),1) AS avgTeamAssists,
                ROUND(AVG(pS.avgSteals),1) AS avgTeamSteals,
                ROUND(AVG(pS.fieldGoalPct),3) AS TeamFGPct,
                ROUND(AVG(pS.threePointPct),3) AS Team3PointPct,
                ROUND(AVG(pS.freeThrowPct),3) AS TeamFreeThrowPct
            FROM TeamWins TW
            JOIN PlayerStats pS ON pS.TeamID= TW.TeamID
            GROUP BY TW.TeamID, TW.TeamName,TW.Wins
        """

    def _team_stats_cte(self):
        return f"""
            WITH TeamWins AS (
                {self._query_team_wins()}
            ),
            PlayerStats AS (
                {self._query_player_stats()}
            ),
            TeamStats AS (
                {self._query_team_stats()}
            )
        """

    def _query_player_age(self):
        return """
            SELECT
                t.TeamID,
                t.TeamName,
                p.PlayerID,
                p.FirstName,
                p.LastName,
                YEAR('2024-6-16') - YEAR(pi.Birthdate) AS playerAge
            FROM PlayerInformation pi
            JOIN Player p ON pi.PlayerID= p.PlayerID
            JOIN Team t ON p.TeamID= t.TeamID
            WHERE IsActive = 1
        """

    def _query_team_avg_age(self):
        return """
            SELECT
                pa.TeamName,
                ROUND(AVG(pa.playerAge),1) as avgTeamAge
            FROM PlayersAge pa
            GROUP BY pa.TeamName
        """

    def get_q1(self, num_teams):
        sql = f"""
            {self._team_stats_cte()}
            SELECT * 
            FROM TeamStats 
            ORDER BY Wins DESC
            OFFSET 0 ROWS
            FETCH NEXT %s ROWS ONLY
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (num_teams,))
            rows = cursor.fetchall()

        return rows

    def get_q2(self):
        sql = """
            WITH vetCoach AS (
                SELECT
                c.CoachName,
                c.CoachID
                FROM Coach c
                WHERE c.SeasonsOverall > 5
            )
            SELECT
                vC.CoachName,
                ROUND(CAST(PGCS.PlayoffsOverallW AS FLOAT)/PGCS.PlayoffsOverallG,3) AS PlayoffWinRate
            FROM vetCoach vC
            JOIN PlayoffGameCoachStats PGCS ON PGCS.CoachID= vC.CoachID
            WHERE PGCS.PlayoffsOverallW > PGCS.PlayoffsOverallL
            ORDER BY PlayoffWinRate DESC; 
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_q3(self, team_name, use_avg):
        if use_avg:
            sql = f"""
                {self._team_stats_cte()}
                SELECT DISTINCT
                    ts.TeamID,
                    ts.TeamName,
                    ts.avgTeamPoints,
                    (
                        SELECT ROUND(AVG(avgTeamPoints), 1) 
                        FROM TeamStats
                    ) AS avgLeaguePoints
                FROM TeamStats ts
                WHERE LOWER(ts.TeamName) = %s;
            """

        else:
            sql = f"""
                {self._team_stats_cte()}
                SELECT DISTINCT
                    TeamID, 
                    TeamName, 
                    avgTeamPoints AS teamAvgPPG
                FROM TeamStats
                WHERE LOWER(TeamName) = %s;
            """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (team_name,))
            rows = cursor.fetchall()

        return rows

    def get_q4(self, num_players, page):
        offset = (page - 1) * num_players
        sql = f"""
            WITH PlayerStats AS (
                {self._query_player_stats()}
            )
            SELECT
                ps.avgPoints,
                ps.avgAssists,
                ps.avgSteals,
                ps.FirstName,
                ps.LastName,
                pi.Height,
                pi.Position
            FROM PlayerStats ps
            JOIN PlayerInformation pi ON ps.PlayerID = pi.PlayerID
            ORDER BY pi.Position, pi.Height
            OFFSET %s ROWS
            FETCH NEXT %s ROWS ONLY;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (offset, num_players))
            rows = cursor.fetchall()

        return rows

    def get_q5(self):
        sql = """
            SELECT
                c.CoachName,
                t.TeamName,
                PGCS.PlayoffsCurrentW as playoffWins
            FROM PlayoffGameCoachStats PGCS
            JOIN Coach c ON PGCS.CoachID= c.CoachID
            JOIN Team t ON c.TeamID= t.TeamID
            WHERE PGCS.PlayoffsCurrentW= 16;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows

    def get_q6(self, team_name):
        sql = f"""
            WITH PlayerStats AS (
                {self._query_player_stats()}
            )
            SELECT
                t.TeamName,
                p.FirstName,
                p.LastName,
                ps.avgPoints,
                ps.avgAssists,
                ps.avgSteals
            FROM Team t
            JOIN Player p ON t.TeamID= p.TeamID
            JOIN PlayerStats ps ON p.PlayerID= ps.PlayerID
            WHERE t.TeamName=%s
            ORDER BY ps.avgPoints DESC,ps.avgAssists DESC,ps.avgSteals DESC;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (team_name,))
            rows = cursor.fetchall()

        return rows

    def get_q7(self, stat, num_players):
        sql = f"""
            WITH PlayerStats AS (
                {self._query_player_stats()}
            )
            SELECT
                ps.FirstName,
                ps.LastName,
                ps.avgPoints,
                ps.avgAssists,
                ps.avgSteals
            FROM PlayerStats ps
            ORDER BY %s DESC
            OFFSET 0 ROWS
            FETCH NEXT %s ROWS ONLY
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (stat, num_players))
            rows = cursor.fetchall()

        return rows

    def get_q8(self, team_name):
        sql = f"""
            WITH PlayersAge AS (
                {self._query_player_age()}
            ),
            GetTeamAvgAge AS (
                {self._query_team_avg_age()}
            )
            SELECT *
            FROM GetTeamAvgAge
            WHERE TeamName = %s;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (team_name,))
            rows = cursor.fetchall()

        return rows

    def get_q9(self, game_id):
        sql = """
        WITH playersGame AS (
            SELECT
                Team.TeamID,
                HomePTS,
                VisitorPTS,
                STL,
                FG,
                FGA,
                "3P",
                "3PA",
                AST,
                FTA,
                FT
            FROM Game
            JOIN PlayInGame ON Game.GameID = PlayInGame.GameID
            JOIN Player ON PlayInGame.PlayerID = Player.PlayerID
            JOIN Team ON Player.TeamID = Team.TeamID
            WHERE Game.GameID = %s
            )
        SELECT
            TeamID,
            MAX(HomePTS) AS HomePTS,
            MAX(VisitorPTS) AS VisitorPTS,
            SUM(STL) AS STL,
            SUM(FG) AS FG,
            SUM(FGA) AS FGA,
            CAST(ROUND(SUM(FG) * 1.0 / NULLIF(SUM(FGA), 0), 3) AS FLOAT) AS FGP,
            SUM("3P") AS "3P",
            SUM("3PA") AS "3PA",
            CAST(ROUND(SUM("3P") * 1.0 / NULLIF(SUM("3PA"), 0), 3) AS FLOAT) AS "3PP",
            SUM(FT) AS FT,
            SUM(FTA) AS FTA,
            CAST(ROUND(SUM(FT) * 1.0 / NULLIF(SUM(FTA), 0), 3) AS FLOAT) AS FTP,
            SUM(AST) AS AST
        FROM playersGame
        GROUP BY TeamID;
        
        """
        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (game_id,))
            rows = cursor.fetchall()

        return rows

    def get_q10(self, min_attempts, num_players):
        sql = """
        SELECT
            Player.PlayerID,
            FirstName,
            LastName,
            CAST(ROUND(SUM("3P") * 1.0 / NULLIF(SUM("3PA"), 0), 3) AS FLOAT) AS "3PP"
        FROM Player
        JOIN PlayInGame ON Player.PlayerID = PlayInGame.PlayerID
        GROUP BY Player.PlayerID, FirstName, LastName
        HAVING SUM("3PA") > %s
        ORDER BY "3PP" DESC
        OFFSET 0 ROWS
        FETCH NEXT %s ROWS ONLY;
        """
        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (min_attempts, num_players))
            rows = cursor.fetchall()

        return rows

    def get_q11(self, game_id):
        sql = """
            WITH PlayerHeights AS (
                SELECT
                    Player.PlayerID as PlayerID,
                    FirstName,
                    LastName,
                    Position,
                    Height,
                    CAST(LEFT(Height, CHARINDEX('"', Height) - 1) AS INT) * 12 
                    +
                    CAST(
                        SUBSTRING(Height, CHARINDEX('"', Height) + 1, LEN(Height))
                        AS INT
                    ) AS HeightInches
                FROM PlayerInformation
                JOIN Player
                ON PlayerInformation.PlayerID = Player.PlayerID
            )
            SELECT 
                FirstName, 
                LastName, 
                Height, 
                ( (FG-[3P])*2 + ([3P] * 3) + (FT) ) as PTS
            FROM PlayerHeights
            JOIN PlayInGame
            ON PlayerHeights.PlayerID = PlayInGame.PlayerID
            WHERE gameID = %s 
                AND
                HeightInches > 77
                AND Position = 'Center';
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (game_id,))
            rows = cursor.fetchall()

        return rows

    def get_q12(self, home_team, away_team):
        sql = """
             WITH FirstTeamID AS(
                SELECT 
                    TeamID
                FROM team
                WHERE 
                    TeamName = %s),
            SecondTeamID AS(
                SELECT 
                    TeamID
                FROM team
                WHERE 
                    TeamName = %s),
            CountAllMatchups AS (
                SELECT 
                    count(DISTINCT g.gameID) as totalMatchups
                FROM game g
                WHERE 
                    (g.HomeTeamID = (SELECT TeamID FROM FirstTeamID) 
                    AND 
                    g.VisitorTeamID = (SELECT TeamID FROM SecondTeamID))
                OR 
                    (g.HomeTeamID = (SELECT TeamID FROM SecondTeamID) 
                    AND 
                    g.VisitorTeamID = (SELECT TeamID FROM FirstTeamID))),
            CountWins AS (
                SELECT 
                    COUNT(DISTINCT g.gameID) AS wins
                FROM game g
                WHERE 
                    (g.HomeTeamID = (SELECT TeamID FROM FirstTeamID) 
                    AND 
                    g.VisitorTeamID = (SELECT TeamID FROM SecondTeamID) 
                    AND 
                    g.HomePTS > g.VisitorPTS)
                OR 
                    (g.HomeTeamID = (SELECT TeamID FROM SecondTeamID) 
                    AND 
                    g.VisitorTeamID = (SELECT TeamID FROM FirstTeamID) 
                    AND 
                    g.VisitorPTS > g.HomePTS))
            SELECT 
                ROUND(
                    CAST((SELECT wins FROM COUNTWINS) AS FLOAT)/
                    NULLIF((select totalMatchups from CountAllMatchups),0),3) * 100 AS winPCT
      
       """
        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (away_team, home_team))
            rows = cursor.fetchall()

        return rows

    def get_q13(self, min_winrate):
        sql = """
            WITH CoachesInRecentPlayoff as(
                SELECT 
                    CoachID
                FROM PlayoffGameCoachStats PGCS
                WHERE PlayoffsOverallG > 0)
                SELECT 
                    CoachName, 
                   ROUND(CAST(PGCS.PlayoffsOverallW AS FLOAT)/ NULLIF(PGCS.PlayoffsOverallG,0),3) AS overallWinRate
                FROM Coach 
                JOIN PlayoffGameCoachStats AS PGCS
                ON Coach.CoachID = PGCS.CoachID
                WHERE (CAST(PGCS.PlayoffsOverallW AS FLOAT)/ NULLIF(PGCS.PlayoffsOverallG,0)) >= %s
                AND 
                PGCS.coachID IN (SELECT CoachID from CoachesInRecentPlayoff)
                ORDER BY overallWinRate DESC; 
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (min_winrate,))
            rows = cursor.fetchall()

        return rows

    def get_q14(self, min_teams):
        sql = """
            WITH TeamWinAtArena AS(
                SELECT Arena, HomeTeamID AS TeamID
                FROM Game
                WHERE 
                    HomePTS > VisitorPTS 
                    AND Arena IS NOT NULL
                UNION
                SELECT Arena, VisitorTeamID as TeamID
                FROM Game
                WHERE 
                    VisitorPTS > HomePTS
                    AND Arena IS NOT NULL
            )
            SELECT Arena, COUNT(TeamID) AS NumTeamsWon
            FROM TeamWinAtArena
            GROUP BY Arena
            HAVING COUNT(TeamID) >= %s
            ORDER BY NumTeamsWon DESC;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql, (min_teams,))
            rows = cursor.fetchall()

        return rows
