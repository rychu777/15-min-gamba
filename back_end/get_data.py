import csv
import time

import requests


def gather_summoner_ids(API_key: str, output_file: str, tier: str = 'CHALLENGER', min_players: int = 200) -> None:
    """
    Gather master tier player data from Riot API and extract summoner encrypted IDs.

    Args:
    :argument: API_key (str): API key for Riot Games API.
    :argument: output_file (str): Path to the output file to write summoner encrypted IDs.
    :argument: min_players (int): Minimum number of players to gather. Although the limit is reached
               we will scrap the remaining players of current page. Defaults to 200.
    :argument: tier (str): Tier from which we want to gather players. Defaults to CHALLENGER

    Returns:
    :return None
    """
    current_page = 1
    total_players_gathered = 0

    while total_players_gathered < min_players:
        response = requests.get(
            f'https://eun1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/I?page={current_page}&api_key={API_key}')
        with open(output_file, 'a') as f:
            for summoner in response.json():
                try:
                    f.write(summoner['summonerId'] + '\n')
                    total_players_gathered += 1
                except UnicodeEncodeError:
                    pass
        time.sleep(1.21)  # Due to Riot API limitations required value is 1.2, 0.01 added for safety :)
        current_page += 1


def extract_puuids(API_key: str, input_file: str, output_file: str) -> None:
    """
    Extract PUUIDs from Riot API using the provided list of summoner encrypted IDs.

    Args:
    :argument: API_key (str): API key for Riot Games API.
    :argument: input_file (str): Path to the input file containing summoner encrypted IDs.
    :argument: output_file (str): Path to the output file to write PUUIDs.

    Returns:
    :return: None
    """
    with open(input_file, 'r') as f:
        summoner_encrypted_ids = f.read().splitlines()

    with open(output_file, 'a') as f:
        for summoner_id in summoner_encrypted_ids:
            try:
                response = requests.get(
                    f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={API_key}')
                f.write(response.json()['puuid'] + '\n')
            except KeyError:
                print(f'Error getting PUUUID from: {summoner_id}')
                pass
            time.sleep(1.21)  # Due to Riot API limitations required value is 1.2, 0.01 added for safety :)


def fetch_match_ids(API_key: str, input_file: str, output_file: str) -> None:
    """
    Fetch match IDs from Riot API using the provided list of PUUIDs.

    Args:
    :argument: API_key (str): API key for Riot Games API.
    :argument: input_file (str): Path to the input file containing PUUIDs.
    :argument: output_file (str): Path to the output file to write match IDs.

    Returns:
    :return: None
    """
    with open(input_file, 'r') as f:
        puuids = f.read().splitlines()

    with open(output_file, 'a') as f:
        for puuid in puuids:
            response = requests.get(
                f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=100&api_key={API_key}')

            for match in response.json():
                f.write(match + '\n')

            time.sleep(1.21)  # Due to Riot API limitations required value is 1.2, 0.01 added for safety :)


def get_match_data(API_key: str, input_file: str, output_file: str) -> None:
    """
    Get specific match data from input_file containing id's of matches.
    Write data in csv file.

    Args:
    :argument: API_key (str): API key for Riot Games API.
    :argument: input_file (str): Path to the input file containing match ID's.
    :argument: output_file (str): Path to the output file to write details about each game.

    Returns:
    :return: None
    """
    with open(input_file, 'r') as file_1:
        matches = file_1.read().splitlines()

    lenOfMatchesToIterate = len(matches)  # Percentage delete later

    with open(output_file, 'a') as file_2:
        writer = csv.writer(file_2, delimiter=',', lineterminator='\n')

        # Iterate over matches while there are still matches to iterate over
        while len(matches) > 0:

            # API call sometimes returns error for no reason at all
            # When querying the same game again it works
            try:

                # Reset values, some add up over iterations
                blueTeamTotalGold = 0
                blueTeamAvgLevel = 0
                blueTeamTotalMinionsKilled = 0
                blueTeamTotalJungleMonstersKilled = 0

                redTeamTotalGold = 0
                redTeamAvgLevel = 0
                redTeamTotalMinionsKilled = 0
                redTeamTotalJungleMonstersKilled = 0

                blueTeamWardsPlaced = 0
                blueTeamWardsDestroyed = 0
                blueTeamTowersDestroyed = 0
                blueTeamDragonsKilled = 0
                blueTeamHeraldsKilled = 0
                blueTeamVoidGrubsKilled = 0
                blueTeamKills = 0
                blueTeamDeaths = 0
                blueTeamAssists = 0

                redTeamWardsPlaced = 0
                redTeamWardsDestroyed = 0
                redTeamTowersDestroyed = 0
                redTeamDragonsKilled = 0
                redTeamHeraldsKilled = 0
                redTeamVoidGrubsKilled = 0
                redTeamKills = 0
                redTeamDeaths = 0
                redTeamAssists = 0

                gameDuration = 0

                # In case no first blood in first 15 min, later to sort out in the df
                blueTeamFirstBlood = 2
                redTeamFirstBlood = 2
                # In case game was too short, later to sort out in the df
                blueTeamWin = 2
                redTeamWin = 2

                print(matches[0], round(((lenOfMatchesToIterate - len(matches)) * 100) / lenOfMatchesToIterate, 2),
                      '%')  # Debug printer

                response = requests.get(
                    f'https://europe.api.riotgames.com/lol/match/v5/matches/{matches[0]}/timeline?api_key={API_key}')
                data = response.json()

                # So python doesn't have to iterate over the whole dictionary each time
                lastEvent = data['info']['frames'][-1]['events'][-1]

                # Check if game is longer than 14.5 minutes (in case of early surrender or buggy return values)
                if lastEvent['timestamp'] > 870000:
                    # blueTeamWin redTeamWin
                    try:
                        if lastEvent['winningTeam'] == 100:
                            blueTeamWin = 1
                            redTeamWin = 0
                        elif lastEvent['winningTeam'] == 200:
                            blueTeamWin = 0
                            redTeamWin = 1
                        else:  # In case something is messed up to check after
                            blueTeamWin = 2
                            redTeamWin = 2
                    except KeyError:
                        blueTeamWin = 2
                        redTeamWin = 2

                    # Game duration, will be saved in seconds
                    gameDuration = (lastEvent['timestamp']) / 1000

                    x = 0  # x Equals every minute in the game
                    while x <= 15:  # Get all information until (including) 15th minute

                        # So python doesn't have to iterate over the whole dictionary each time
                        events = data['info']['frames'][x]['events']

                        # Iterates over each event in a game
                        for y in range(len(events)):
                            # Wards placed check
                            if events[y]['type'] == 'WARD_PLACED':
                                if 1 <= events[y]['creatorId'] <= 5:
                                    blueTeamWardsPlaced += 1
                                elif 6 <= events[y]['creatorId'] <= 10:
                                    redTeamWardsPlaced += 1
                            # Wards destroyed check
                            if events[y]['type'] == 'WARD_KILL':
                                if 1 <= events[y]['killerId'] <= 5:
                                    blueTeamWardsDestroyed += 1
                                elif 6 <= events[y]['killerId'] <= 10:
                                    redTeamWardsDestroyed += 1
                            # Towers destroyed check
                            if events[y]['type'] == 'BUILDING_KILL':
                                if events[y]['buildingType'] == 'TOWER_BUILDING':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamTowersDestroyed += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamTowersDestroyed += 1
                            # Elite jungle monster check (Dragon / Herald / Void grubs)
                            if events[y]['type'] == 'ELITE_MONSTER_KILL':
                                # Dragon
                                if events[y]['monsterType'] == 'DRAGON':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamDragonsKilled += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamDragonsKilled += 1
                                # Herald
                                if events[y]['monsterType'] == 'RIFTHERALD':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamHeraldsKilled += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamHeraldsKilled += 1
                                # Void grubs
                                if events[y]['monsterType'] == 'HORDE':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamVoidGrubsKilled += 1
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        redTeamVoidGrubsKilled += 1
                            # Kills / Deaths
                            if events[y]['type'] == 'CHAMPION_KILL':
                                if 1 <= events[y]['killerId'] <= 5:
                                    blueTeamKills += 1
                                    redTeamDeaths += 1
                                    if 'assistingParticipantIds' in events[y]:
                                        blueTeamAssists += len(
                                            events[y]['assistingParticipantIds'])
                                elif 6 <= events[y]['killerId'] <= 10:
                                    blueTeamDeaths += 1
                                    redTeamKills += 1
                                    if 'assistingParticipantIds' in events[y]:
                                        redTeamAssists += len(
                                            events[y]['assistingParticipantIds'])
                            # First blood check
                            if 'killType' in events[y]:
                                if events[y]['killType'] == 'KILL_FIRST_BLOOD':
                                    if 1 <= events[y]['killerId'] <= 5:
                                        blueTeamFirstBlood = 1
                                        redTeamFirstBlood = 0
                                    elif 6 <= events[y]['killerId'] <= 10:
                                        blueTeamFirstBlood = 0
                                        redTeamFirstBlood = 1

                        # So python doesn't have to iterate over the whole dict each time
                        participants = data['info']['frames'][x]['participantFrames']

                        # Check timestamp values
                        if 900000 < data['info']['frames'][x]['timestamp'] < 901000:  # See readme for range explanation
                            for participant in participants:
                                # Blue team
                                if int(participant) <= 5:
                                    blueTeamTotalGold += participants[participant][
                                        'totalGold']
                                    blueTeamAvgLevel += participants[participant]['level']
                                    blueTeamTotalMinionsKilled += participants[participant][
                                        'minionsKilled']
                                    blueTeamTotalJungleMonstersKilled += participants[participant][
                                        'jungleMinionsKilled']
                                # Red team
                                else:
                                    redTeamTotalGold += participants[participant][
                                        'totalGold']
                                    redTeamAvgLevel += participants[participant]['level']
                                    redTeamTotalMinionsKilled += participants[participant][
                                        'minionsKilled']
                                    redTeamTotalJungleMonstersKilled += participants[participant][
                                        'jungleMinionsKilled']
                        x += 1  # Increase to check next timestamp

                # Get average team level
                blueTeamAvgLevel = blueTeamAvgLevel / 5
                redTeamAvgLevel = redTeamAvgLevel / 5
                # Get average team cs
                blueTeamCsPerMinute = (blueTeamTotalMinionsKilled + blueTeamTotalJungleMonstersKilled) / 15
                redTeamCsPerMinute = (redTeamTotalMinionsKilled + redTeamTotalJungleMonstersKilled) / 15
                # Get average team gold
                blueTeamGoldPerMinute = blueTeamTotalGold / 15
                redTeamGoldPerMinute = redTeamTotalGold / 15
                # Get average wards placed
                blueTeamWardsPlaced = blueTeamWardsPlaced / 5
                redTeamWardsPlaced = redTeamWardsPlaced / 5
                # Get average wards destroyed
                blueTeamWardsDestroyed = blueTeamWardsDestroyed / 5
                redTeamWardsDestroyed = redTeamWardsDestroyed / 5

                # This will be written to csv file, some values rounded for data readability
                writeToFile = [
                    blueTeamTotalJungleMonstersKilled, blueTeamTotalMinionsKilled, blueTeamTowersDestroyed,
                    blueTeamVoidGrubsKilled, round(blueTeamWardsDestroyed, 2), blueTeamDragonsKilled,
                    blueTeamHeraldsKilled,
                    round(blueTeamGoldPerMinute, 2), round(blueTeamWardsPlaced, 2), round(blueTeamCsPerMinute, 2),
                    blueTeamFirstBlood,
                    blueTeamTotalGold, round(blueTeamAvgLevel, 2), blueTeamAssists, blueTeamDeaths, blueTeamKills,
                    blueTeamWin,
                    redTeamTotalJungleMonstersKilled, redTeamTotalMinionsKilled, redTeamTowersDestroyed,
                    redTeamVoidGrubsKilled, round(redTeamWardsDestroyed, 2), redTeamDragonsKilled, redTeamHeraldsKilled,
                    round(redTeamGoldPerMinute, 2), round(redTeamWardsPlaced, 2), round(redTeamCsPerMinute, 2),
                    redTeamFirstBlood,
                    redTeamTotalGold, round(redTeamAvgLevel, 2), redTeamAssists, redTeamDeaths, redTeamKills,
                    redTeamWin, gameDuration
                ]

                matches.pop(0)  # Removes currently checked game from the list
                writer.writerow(writeToFile)
                time.sleep(1.21)  # Due to Riot API limitations required value is 1.2, 0.01 added for safety :)
            except KeyError:
                print('Key error occurred.')
                time.sleep(5)
