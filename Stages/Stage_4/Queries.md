# Project Stage 4 - Queries

## English Queries (non trivial)

1. Return the top 10 teams and some simple stats ( avg ppg, apg, etc) according to Wins
2. Return the coaches that have coached more than
   5 seasons with a positive win rate in the playoffs
   - order by winrate
3. Return the average ppg for a specific team, with the option to
   return the avg ppg for the league
4. return all players and their ppg,apg and rpg for the season
   - Group by position and height within
     that position
     - within positions order by the most important stat ( maybe ) .
       Ex. pg ordered by apg then ppg, sg and sf ordered by ppg then rpg,
       pf and center ordered by rpg then ppg
5. return the team and corresponding coach that won the championship that year
   - aggregate functions max and count on playoff wins,
6. list the roster of a team ordered by ppg, should also show
   apg and spg
   - in case of a tie the tie breaker should be apg, then spg
7. return the top 10 players in each major category:
   ppg, apg, spg
8. for a team return the average age of their players
   - maybe extend this to connect with other Queries
     - ex. Maybe we want to see the average age of the top
       10 teams by wins
9. return both teams stats for a specific game
10. list the top 20 players in the league for 3 point percentage
    - player must have over 100 attempts to be included
11. List the players PTS in a game that have a height over 6ft 5in and play the position of center
    - Maybe filter by a couple shooting positions that should have high points
12. Return the win % from one team to another

## justifications

1. this will allow a analyst to quickly see the top performers
   for the season and the relevant important stats
2. This query will allow a analyst to select the coaches the
   best in the playoffs
3. This enables a analyst to grab the most important stat from a team
   while also having the option to compare it's result to the average of the
   league
4. this is an important query because it allows a analyst to retrieve
   the primary stats for all players in the league while grouping them
   according to the role they play in their team
5. less useful for an analyst since they probably already know this
   but I think it must be a part of a sports database
6. an analyst would find this useful since it allows them to evaluate the
   most important contributors to a teams scoring
7. allows an analyst to retrieve the leaders of the 3 major statistical
   categories
8. allows an analyst to evaluate weather a team should start considering
   rebuilding or push for a championship, while also evaluating a teams future.
9. this query allows an analyst to evaluate individual games and each
   teams performance
10. This is a fun cool stat but it also allows an analyst to find the best
    volume 3 point shooters in the league
11. This query allows an analyst to evaluate the performance of centers
    as well as potentially allow an analyst to see if height is correlated with ppg
12. this query allows an analyst to evaluate how well one team performs against
    another

## Note

There will also be simple queries to retrieve individual tables. This will be
done to ensure all data remains accessible
