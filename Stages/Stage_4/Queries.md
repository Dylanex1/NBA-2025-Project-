# Project Stage 4 - Queries

## English Queries

1. Return the top 10 teams according to Wins
   - order by wins
2. Return the coaches that have coached more than
   5 seasons with a positive win rate in the playoffs
   - order by winrate
3. Return the average ppg for a specific team, with the option to
   return the avg ppg for the league
4. return all players and their ppg,apg and rpg for the season
   - Group by position and height within
     that position
     - within positions order by the most important stat.
       Ex. pg ordered by apg then ppg, sg and sf ordered by ppg then rpg,
       pf and center ordered by rpg then ppg
5. return the team and corresponding coach that won the championship that year
   - aggregate functions max and count on playoff wins,
6. list the roster of a team ordered by ppg,
   - in case of a tie the tie breaker should be apg, then rpg
7. return the top 10 players in each major category:
   ppg, apg, rpg
8. for a team return the average age of their players
   - maybe extend this to connect with other Queries
     - ex. Maybe we want to see the average age of the top
       10 teams by wins
9. return the team stats for a specific game
10. list the top 20 players in the league for 3 point percentage
    - player must have over 100 attempts to be included
11. List the players PTS in a game that have a height over 6ft 5in and play the position of center
    - Maybe filter by a couple shooting positions that should have high points
