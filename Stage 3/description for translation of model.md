## Preliminary cleaning process of tables

First and foremost we have cleaned every attribute we did not use in our ER/EER diagram. There was some redundancy in some of the tables and atrributes we did not want to use since our ER diagram was large enough. We have made sure that the columns represent their names as in the ER diagram as well

* Changed column names in `teams.csv` to match all attributes in my ER diagram no columns were removed
* Removed column `full name` in `player.csv` since we have first name and last name already in place. Column `id` got changed to `PlayerID`.
* Made table `Game.csv` and removed `NBA_24_25_Schedule.csv` Since we wanted to be more clear when designing the ER diagram. Added column `GameID` in `Game.csv` to make the games easily identifiable. There were a few empty columns, we dropped and renamed the columns appropriate to match the ER diagram. We added a result for home if they win or lose.
* In `Draft_History.csv` is our `drafts` relationship. We removed column `Player_profile_flag` and we will keep some of the redundancy for now for the normalization steps. For example having `team_city` and `team_abbreviation` in here when its already in `Team.csv`
* In `draft_combine_stats.csv` we decided to remove a lot of columns to match what attributes we have for the ER model. There is some redundancy we will keep for the normalization steps
* For `database_24_25.csv`, it will now be renamed `play in.csv` since there is all the stats in a player's game. There were additional attributes that we removed that were not used in the ER model. There is also redundancy that we will keep in here until the normalization step.
* `Common_Player_info.csv` is known as our `Player information` entity type we removed every column to do with name and only kept the attributes we have in the ER model. We have also had to fix the format of height since it was recognized as a date. 
* `Coaches_24_25.csv` Added coachID in this since  it was not added from before I will leave some redundancy in there for the normalization process.
* `Arenas.csv` some redundancy is in there till the normalization part but the rest of the columns are being left in there.

* All columns in our dataset have no blank values and are filled with 0 or NULL as appropriate.



## Normalization and merging

For this part all entities and their relationships will follow a series of steps on how we execute an EER model to a BCNF merged relational model

1. Translate ER model into relational model </br>

The first thing that we did was make sure that the dataset was cleaned. The next thing that was focused on was to draw out the sets and what each relationship contained.


2. Normalization steps
    * 1NF


    * 2NF

    * 3NF

    * BCNF 

3. Merging process