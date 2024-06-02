15-min-gamba
# Data science project based on League of Legends
## Table of Content
- [Project Object](#project-object)
- [Introduction](#introduction)
- [Collecting the Data](#collecting-the-data)
- [The Match Data](#the-match-data)
- [Data Cleaning](#data-cleaning)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Feature Engineering](#feature-engineering)
- [Possible Multicollinearity](#possible-multicollinearity)
- [Bulding the Model](#building-the-model)
- [Evaluation](#evaluation)
- [Review](#review)
- [Perspectives](#perspectives)

## Project Object

The goal of the project is to effectively predict the outcome of a League of Legends game based on the state of the game at the 15 minutes mark.

## Introduction
League of Legends (LoL) is a highly popular online multiplayer battle arena video game developed and published by Riot Games. It's a free-to-play game that was first released in 2009, and since then, it has become one of the most prominent and influential games in the esports industry.

In League of Legends, players assume the role of a "champion," each with their own unique abilities and playstyles, and are placed into teams of typically five players. The objective varies depending on the game mode, but generally involves destroying the opposing team's Nexus, a structure located within their base. Players must navigate through various lanes and engage in strategic battles with both computer-controlled minions and enemy champions to achieve victory.

One of the key aspects of League of Legends is its strategic depth and complexity. Matches require teamwork, coordination, and skillful execution of individual abilities and tactics. The game also features a constantly evolving meta-game, with frequent updates, balance changes, and new champions being introduced to keep the gameplay fresh and engaging.

## Collecting the Data
In my project I used data from 1000 best players. But why? Simply because good players and extremely good players are making way less mistakes. This means that if they get a lead they are less likely to make risky decision which may result in throwing the winning position they managed to acquire.

All the data I collected was obtained using the Riot Games [API's](https://developer.riotgames.com/apis). They offer a wide range of endpoints that you can use together with the documentation.

However, Riot Games has the following API access rates limits:
- 20 requests every 1 second
- 100 requests every 2 minutes

### Process of coleccting data
```mermaid
  flowchart LR;
      Getting-summoner_ids-->Getting-puuids;
      Getting-puuids-->Getting-match_ids;
      Getting-match_ids-->Getting-match-details;
```
The first step was acquiring the encrypted summoner id's. I could get that by using the 'LEAGUE-EXP-V4' endpoint (specifically, /lol/league-exp/v4/entries/{queue}/{tier}/{division}). Providing the type of queue, rank, and number of pages I could get a list containing id's mentioned earlier. I chose to get id's of a **1000** best players from EUNE (Europe Nordic East) server. Precisely I got **200** CHALLENGER, **500** GRANDMASTER and **300** MASTER rank players.

The second step was to convert my **1000** summoner id's into PUUID's, which are another type of ID, this time used to connect players to the game. I managed to do this using the 'SUMMONER-V4' endpoint (specifically, /lol/summoner/v4/summoners/{encryptedSummonerId}), which after sending the summoner id returned the corresponding PUUID.

Now for each player, with the help of the already acquired PUUID I had to acquire his history of ranked games . The ones on which he was classified. To do this, a 'MATCH-V5' endpoint was needed. (specifically, /lol/match/v5/matches/by-puuid/{puuid}/ids) After entering a player's PUUID, it returned his game history in the form of id's of his **100** most recently played ranked games. (**100** was the limit for each player) The process resulted in me getting **100 000** game id's played by the best players on the server.

However, as you can guess, since these are the best players, they play with each other. After checking and removing duplicate game id's. From **100 000** game id's, I was left with only **42172** left (**58.8%** of data was removed}).

### Summarisation:
- I used my self-gathered data
- I got the data with Riot Game's API using different endpoints
- I used 100 games per player out of 1000 player base
- I ended up with around 42 000 match entries in my data set

## The Match Data

This section is about designind the data frame.

When querying a match with a timeline with the average game duration (which was around **28.1** minutes on EUNE server), the returning JSON file included about **37k** (thirty-seven thousand) lines, which was way too much to put in this README.
Therefore, I decided to display a simplified 'pseudo'-version of it for you to be able to follow up:

    metadata
        match id
        participants
    info
        event
            event type
            timestamp
            additional event info
        stats
            player 1
            player 2
            ...
            player 10
            timestamp
        event
            event type
            timestamp
            additional event info
        stats
            player 1
            player 2
            ...
            player 10
            timestamp
        ...

Note that there was a new 'event' and 'stats' entries every minute. That means, including the 0th minute, there were 1 + 28 'event'/'stats' entries in a match with a duration of 28 minutes.
I focused on only the 'stats' at the 15-minute timestamp since that includes the values I want.

The timestamps are in milliseconds and sadly there is not always the same timestamp at the exactly 15-minute mark.
An example was game when timestamp occured at **900207** miliseconds, which was around **15.00345** minutes.
I couldn't look at a decent amount of games to be able to confidently define the average of the 15-minute timestamp, so I used 900000-901000 milliseconds (or 15-15,0166667 minutes).
Here is an example of the 'stats' of one player at a certain timestamp:

    "1": {
        "championStats": {
            "abilityHaste": 0,
            "abilityPower": 0,
            "armor": 42,
            "armorPen": 0,
            "armorPenPercent": 0,
            "attackDamage": 73,
            "attackSpeed": 127,
            "bonusArmorPenPercent": 0,
            "bonusMagicPenPercent": 0,
            "ccReduction": 5,
            "cooldownReduction": 0,
            "health": 685,
            "healthMax": 685,
            "healthRegen": 17,
            "lifesteal": 0,
            "magicPen": 0,
            "magicPenPercent": 0,
            "magicResist": 32,
            "movementSpeed": 350,
            "omnivamp": 0,
            "physicalVamp": 0,
            "power": 339,
            "powerMax": 339,
            "powerRegen": 15,
            "spellVamp": 0
        },
        "currentGold": 98,
        "damageStats": {
            "magicDamageDone": 0,
            "magicDamageDoneToChampions": 0,
            "magicDamageTaken": 0,
            "physicalDamageDone": 440,
            "physicalDamageDoneToChampions": 0,
            "physicalDamageTaken": 0,
            "totalDamageDone": 440,
            "totalDamageDoneToChampions": 0,
            "totalDamageTaken": 0,
            "trueDamageDone": 0,
            "trueDamageDoneToChampions": 0,
            "trueDamageTaken": 0
        },
        "goldPerSecond": 0,
        "jungleMinionsKilled": 0,
        "level": 1,
        "minionsKilled": 4,
        "participantId": 1,
        "position": {
            "x": 2206,
            "y": 12847
        },
        "timeEnemySpentControlled": 0,
        "totalGold": 598,
        "xp": 211
    }
Here is the list of data I wanted to gather:

| **Value**                | **Explanation**                                                                    | **Where/How to get**                                                                        |
|--------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| win                      | Which team did win                                                                 | 'GAME_END'-event                                                                            |
| wardsPlaced              | A ward provides vision and might prevent death                                     | Iterate over each 'WARD_PLACED'-event and add up                                            |
| wardsDestroyed           |                                                                                    | Iterate over each 'WARD_KILL'-event and add up                                              |
| firstBlood               | The first kill in a game provides extra gold                                       | 'killType': 'KILL_FIRST_BLOOD'                                                              |
| kills                    | Provides gold and experience and prevents enemy from gathering gold and experience | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'killerID'                       |
| deaths                   |                                                                                    | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'victimID'                       |
| assists                  | Provides a tiny bit of gold and experience                                         | Iterate over each 'type': 'CHAMPION_KILL' and add 'assistingParticipantIds'                 |
| dragons                  | Provides team-wide buff, gold and experience                                       | Iterate over each 'monsterType': 'DRAGON' and read 'killerTeamId'                           |
| heralds                  | Once killed, a herald can be placed to destroy buildings                           | Iterade over each 'monsterType': 'RIFTHERALD' and read 'killerTeamId'                       |
| voidGrubsKilled          | Once killed, increases the damege dealt to towers                                  | Iterate over each 'monsterType': 'HORDE' and read 'killerTeamId'                            |
| towersDestroyed          | Provides gold, opens the map                                                       | Iterate over each 'type': 'BUILDING_KILL' where 'buildingType': 'TOWER_BUILDING'            |
| totalGold                | Gold is required to purchase items                                                 | Read 'totalGold' from 'stats' per player                                                    |
| avgLevel                 | Player get better stats when advancing to the next level                           | Read 'level' for each summoner and divide by 5                                              |
| totalMinionsKilled       | Minions provide gold and experience                                                | Read 'minionsKilled' and add up for each player                                             |
| totalJungleMonsterKilled | Jungle monster provide gold and experience                                         | Read 'jungleMinionsKilled' and add up for each player                                       |
| csPerMinute              | Amount of minions killed per minute                                                | Add totalMinionsKilled for each player, divide by 5, divide by 15                           |
| goldPerMinute            | Amount of gold acquired per minute                                                 | Read 'goldPerSecond' for each player, add up and divide by 5                                |
| gameDuration             |                                                                                    | 'GAME_END'-event                                                                            |


The table below shows my variables and their data types:

| **Variable**                     | **Datatype** |
|----------------------------------|--------------|
| blueTeamWin                      | integer      |
| blueTeamWardsPlaced              | float        |
| blueTeamWardsDestroyed           | float        |
| blueTeamFirstBlood               | integer      |
| blueTeamKills                    | integer      |
| blueTeamDeaths                   | integer      |
| blueTeamAssists                  | integer      |
| blueTeamDragons                  | integer      |
| blueTeamVoidGrubsKilled          | intefer      |
| blueTeamHeralds                  | integer      |
| blueTeamTowerDestroyed           | integer      |
| blueTeamTotalGold                | integer      |
| blueTeamAvgLevel                 | float        |
| blueTeamTotalMinionsKilled       | integer      |
| blueTeamTotalJungleMonsterKilled | integer      |
| blueTeamCsPerMinute              | float        |
| blueTeamGoldPerMinute            | float        |
| gameDuration (in seconds)        | integer      |

Please note, there were the same variables for the red team aswell (excluding gameDuration obviously).
blueTeamWin was numeric value: 1 for True and 0 for False, to simplify the handling in the dataframe later.
Collected raw data was stored originally in .csv file.

The last step was saving the raw match data I got.
Now there are different ways of storing dataframes. The direct comparison shows [feather](https://arrow.apache.org/docs/python/feather.html) to be the optimal storage file-format:

![dataframes-storage-comparison](readme-resources/storage-comparison.png)

([Source.](https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d)

## Data Cleaning





