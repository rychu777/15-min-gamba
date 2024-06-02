15-min-gamba
# Data science project based on League of Legends
## Table of Content
- [Project Object](#project-object)
- [Introduction](#introducion)
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

When querying a match with a timeline with the average game duration (which is around *28.1* minutes on EUNE server), the returning JSON file includes about **37k** (thirty-seven thousand) lines, which is way too much to this README. 
Therefore, I will display a simplified 'pseudo'-version of it for you to be able to follow up:

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


