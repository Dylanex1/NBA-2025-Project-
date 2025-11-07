# Queries translated into SQL statements

## First Query

> Note: \
> ? - is used to indicate the spot where user input would be used

- Return the top 10 teams and some simple stats
  ( avg ppg, apg, etc) according to Wins

> First define a view to get team wins

```sql
CREATE VIEW TeamWins AS
SELECT
    t.Team_ID,
    t.Team_Name,
    RGCS.Reg_Current_W AS Wins
FROM RegularGameCoachStats RGCS

JOIN Coach c ON RGCS.CoachID = c.CoachID
JOIN Team t ON c.Team_ID = t.Team_ID;
```

> Then find a view for player averages

```sql
CREATE VIEW PlayerStats AS
SELECT
    p.PlayerID,
    p.Team_ID,
    p.first_name,
    p.last_name,
    --basic stats
    COUNT(pi.GameID) AS games_played,
    ROUND(AVG(pIN.PTS),1) AS avgPoints,
    ROUND(AVG(pIN.AST),1) AS avgAssists,
    ROUND(AVG(pIN.STL),1) AS avgSteals,
    -- more advanced stats
    ROUND(AVG(pIN.MP),1) AS avgMinutesPlayed,
    ROUND(AVG(pIN.FG), 1) AS avgFieldGoalsMade,
    ROUND(AVG(pIN.FGA), 1) AS avgFieldGoalsAttempted,
    ROUND(AVG(pIN.3P), 1) AS avgThreePointersMade,
    ROUND(AVG(pIN.3PA), 1) AS avgThreePointersAttempted,
    ROUND(AVG(pIN.FT), 1) AS avgFreeThrowsMade,
    ROUND(AVG(pIN.FTA), 1) AS avgFreeThrowsAttempted,
    -- now derived stats
    ROUND(SUM(pIN.FG) / NULLIF(SUM(pIN.FGA), 0), 3) AS fieldGoalPct,
    ROUND(SUM(pIN.3P) / NULLIF(SUM(pIN.3PA), 0), 3) AS threePointPct,
    ROUND(SUM(pIN.FT) / NULLIF(SUM(pIN.FTA), 0), 3) AS freeThrowPct
From Player p
JOIN Play_in pIN ON p.PlayerID = pIN.PlayerID
GROUP BY p.PlayerID, p.NAME, p.Team_ID;

```

- Should we use Common table Expression or Views
  Finally we can find ?
- should all we make all our queries views ?

> Finally we can find return the top teams and their corresponding stats

```sql
CREATE VIEW TeamStats AS
Select
    TW.Wins,
    TW.Team_Name,
    TW.Team_ID,
    ROUND(AVG(pS.avgPoints),1) AS avgTeamPoints,
    ROUND(AVG(pS.avgAssists),1) AS avgTeamAssists,
    ROUND(AVG(pS.avgSteals),1) AS avgTeamSteals,
    ROUND(AVG(pS.fieldGoalPct),3) AS TeamFGPct,
    ROUND(AVG(pS.threePointPct),3) AS Team3PointPct,
    ROUND(AVG(pS.freeThrowPct),3) AS TeamFreeThrowPct

From TeamWins TW
JOIN PlayerStats pS ON pS.Team_ID = TW.Team_ID
GROUP BY TW.Team_ID, TW.Team_Name,TW.Wins
ORDER BY TW.Wins DESC
Limit ?;
-- replaced in the java or python code we make to present the query
```

- ? Is this ok as a standin, I did this as this is how it was done
  in the assignment

## Second Query

- Return the coaches that have coached more than
  5 seasons with a positive win rate in the playoffs
  - order by winrate

```sql
WITH vetCoach AS (
SELECT
    c.Coach_name,
    c.CoachID
FROM Coach c
WHERE c.Seasons_Overall > 5)

SELECT
    vC.Coach_name,
    ROUND(CAST(PGCS.Playoffs_Overall_W AS FLOAT)/PGCS.Playoffs_Overall_G,3) AS PlayoffWinRate

FROM vetCoach vC
JOIN PlayoffGameCoachStats PGCS ON PGCS.CoachID = vC.CoachID
WHERE PGCS.Playoffs_Overall_W > PGCS.Playoffs_Overall_L
ORDER BY PlayoffWinRate DESC;
```

- should names match EER diagram or our datasets

## Third Query

- Return the average ppg for a specific team, with the option to
  return the avg ppg for the league

> I will use the TeamStats view I defined earlier to easily retrieve the
> ppg for a specific team

```sql
SELECT Team_Name, avgTeamPoints AS teamAvgPPG
FROM TeamStats
WHERE Team_Name = ?;
```

> Option for the league average

```sql
SELECT
    ts.Team_Name,
    ts.avgTeamPoints,
    ts.Team_ID,
  ( SELECT ROUND(AVG(ts.avgTeamPoints),1) FROM ts.TeamStats )AS avgLeaguePoints

FROM TeamStats ts
WHERE ts.TeamName = ?;
```

- ? standin for user input

## forth query

- return a user defined amount players and their ppg,apg and spg for the season
  - Group by position and order by height within
    that position

> changed this from the original query as it was trying to do to much while
> also requiring stats that don't exist

```sql
SELECT
    ps.avgPoints,
    ps.avgAssists,
    ps.avgSteals,
    cpi.Height,
    cpi.Position,
    cpi.PlayerID
FROM PlayerStats ps
JOIN common_player_inf cpi ON ps.PlayerID = cpi.PlayerID
ORDER BY cpi.Position, cpi.height
LIMIT ?;
```

## fifth Query

- return the team and corresponding coach that won the championship that year
  - aggregate functions max on playoff wins,

```sql
SELECT
    PGCS.CoachID,
    c.TeamID,
    t.Team_name,
    PGCS.Playoffs_Current_W as playoffWins
FROM PlayoffGameCoachStats PGCS
JOIN Coach c ON PGCS.CoachID = c.CoachID
JOIN Team t ON c.Team_ID = t.Team_ID
-- 16 wins means they won 4 games in each of the 4 rounds, meaning they won
-- the championship
WHERE PGCS.Playoffs_Current_W = 16;
```

## sixth query

- list the roster of a team ordered by ppg, should also show
  apg and spg
  - in case of a tie the tie breaker should be apg, then spg

```sql
SELECT
    t.Team_ID,
    t.Team_Name,
    p.PlayerID,
    p.first_name,
    p.last_name,
    ps.avgPoints,
    ps.avgAssists,
    ps.avgSteals
FROM Team t
JOIN Player p ON t.Team_ID = p.TeamID
JOIN PlayerStats ps ON p.PlayerID = ps.PlayerID
WHERE t.Team_ID = ?
ORDER BY ps.avgPoints DESC,ps.avgAssists DESC,ps.avgSteals DESC;
```

## 7th query

- return the top 10 players in each major category:
  ppg, apg, spg

> Use player stat view from earlier

```sql
SELECT
    ps.first_name,
    ps.last_name,
    ps.avgPoints,
    ps.avgAssists,
    ps.avgSteals
FROM PlayerStats ps
ORDER BY ps.avgPoints DESC
Limit ?;

```

```sql
SELECT
    ps.first_name,
    ps.last_name,
    ps.avgPoints,
    ps.avgAssists,
    ps.avgSteals
FROM PlayerStats ps
ORDER BY ps.avgAssists DESC
Limit ?;
```

```sql
SELECT
    ps.first_name,
    ps.last_name,
    ps.avgPoints,
    ps.avgAssists,
    ps.avgSteals
FROM PlayerStats ps
ORDER BY ps.avgSteals DESC
Limit ?;
```

## 8th Query

- for a team return the average age of their players
  - maybe extend this to connect with other Queries
    - ex. Maybe we want to see the average age of the top
      10 teams by wins
- Note this is the age of the player per the end of the season

> made it a view so it would be easy to connect with other queries in the
> future if we wanted

```sql
CREATE VIEW GetTeamAvgAge AS
WITH PlayersAge AS(
SELECT
    t.Team_ID,
    t.Team_Name,
    p.PlayerID,
    p.first_name,
    p.last_name,

    YEAR('2024-6-16') - YEAR(cpi.birthdate) AS playerAge
    -- assuming playoffs end in june
FROM common_player_inf cpi
JOIN Player p ON cpi.PlayerID = p.PlayerID
JOIN Team t ON p.Team_ID = t.Team_ID
)
SELECT
    pa.Team_Name,
    ROUND(AVG(pa.playerAge),1) as avgTeamAge
FROM PlayersAge pa
GROUP BY pa.Team_Name;

```

Actual query that would take user input

```sql
SELECT * FROM GetTeamAvgAge WHERE Team_Name = ?;
```



## 11th query 

List the players name and PTS in a game (can be chosen) that have a height over 6ft 5in and play the position of center

```sql

SELECT first name, last name, ( (FG-3P)*2 + (3P * 3) + (FT) ) as PTS
FROM commonPlayerInfo CPI JOIN Player
ON CPI.PlayerID = Player.PlayerID
JOIN playsIn
ON Player.PlayerID = playsIn.PlayerID
WHERE gameID = ? AND
CPI.height > '6"5'
AND CPI.position = 'Center';

```

## 12th query

Return the win % from one home team to a visiting team


```sql
--first filter the games only played by those 2 teams maybe not by team id
WITH FirstTeamID AS
(SELECT Team_id
FROM team
WHERE Team_name = ?),
SecondTeamID AS
(SELECT Team_id
FROM team
WHERE Team_name = ?),
-- get a count of how many games they played
CountAllMatchups AS (SELECT count(gameID)
FROM
game WHERE
homeTeamID = firstTeamID
AND visitorTeamID = SecondTeamID)
SELECT (count(gameID)/CountAllMatchups) * 100 AS winPCT
FROM game
WHERE HomePTS > VisitorPTS
AND homeTeamID = firstTeamID
AND visitorTeamID = SecondTeamID; - gets the win %

```

## 13th query 
List the coach names who have made it to the 2024-2025 season playoffs and have a overall playoff win % at least as high as the user input, order coach's from playoff win % from best to worst.

```sql
--List all coachIDs that have made it in the playoffs you have to have Playoffs_overall_W > 0 
WITH CoachesInRecentPlayoff as
(SELECT CoachID
FROM PlayoffGameCoachStats PGCS
WHERE Playoffs_Overall_G > 0)
-- Select the coaches that made the playoffs and have a sufficent overall win rate as the user requested
SELECT Coach_name, (PGCS.Playoffs_Overall_W / PGCS.Playoffs_Overall_G) AS overallWinRate
FROM Coach JOIN PlayoffGameCoachStats AS PGCS
ON Coach.CoachID = PGCS.CoachID
WHERE  overallWinRate >= ?
AND PGCS.coachID IN (CoachesInRecentPlayoff)
ORDER BY overallWinRate DESC;
```



## Simple Queries to retrieve tables

1. List every player draft combine stats that has attended in any draft combine

```sql
SELECT *
FROM DraftCombine
```
  
3. List all drafts in every season from the drafts table

```sql
SELECT *
FROM Drafts
```

4. List every coach with their regular game stats and their Playoff game stats

```sql
SELECT *
FROM Coach AS C
JOIN RegularGameCoachStats RGCS
ON C.CoachID = RGCS.CoachID
JOIN PlayoffGameCoachStats AS PGCS
ON C.CoachID = PGCS.CoachID
```
5. List all Arenas in the dataset

```sql
SELECT *
FROM Arena
```

6. List all Teams in the dataset

```sql
SELECT *
FROM Team
```

7. List all Games in the dataset

```sql
SELECT *
FROM Game
```
8. List all Players with their Player Information in the Dataset

```sql
SELECT *
FROM Player
LEFT JOIN PlayerInformation
ON Player.PlayerID = PlayerInformation.PlayerID
```



