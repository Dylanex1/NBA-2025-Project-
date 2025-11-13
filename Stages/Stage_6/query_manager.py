class QueryManager:
    def __init__(self, connection):
        self._connection = connection

    def get_s1(self):
        sql = """
            SELECT * 
            FROM DraftCombine;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows
    
    def get_s2(self):
        sql = """
            SELECT * 
            FROM Drafts;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
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
        
    def get_s7(self):
        sql = """
            SELECT * 
            FROM Game;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows
        
    def get_s8(self):
        sql = """
            SELECT *
            FROM Player
            LEFT JOIN PlayerInformation
            ON Player.PlayerID= PlayerInformation.PlayerID;
        """

        with self._connection.cursor(as_dict=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        return rows
        
        
        
