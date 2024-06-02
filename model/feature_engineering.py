import pandas as pd


def prepare_data(input_file: str, output_location: str) -> None:
    """
    Prepares the data for machine learning by calculating various statistics and splitting it into training
    and testing sets.

    This function performs the following steps:
    1. Reads data from a Feather file.
    2. Creates a new DataFrame with calculated differences and ratios for blue team metrics.
    3. Saves the prepared DataFrame to a CSV file.
    4. Splits the DataFrame into training, validation and testing sets.
    5. Saves the training, validation and testing sets to separate CSV files.

    Arguments:
    :argument: input_file (str): The path to the input Feather file containing the original data.
    :argument: output_location (str): The directory where the output CSV files will be saved.

    Returns:
    :return: None
    """
    df = pd.read_feather(input_file)
    df2 = pd.DataFrame()
    df2['blueTeamWardRetentionRatio'] = (df.blueTeamWardsPlaced - df.redTeamWardsDestroyed)/df.blueTeamWardsPlaced
    df2['redTeamWardRetentionRatio'] = -1 * (df.redTeamWardsPlaced - df.blueTeamWardsDestroyed)/df.redTeamWardsPlaced
    df2['blueTeamNetKills'] = (df.blueTeamKills - df.redTeamKills)
    df2['blueTeamTeamWorkGradeDiff'] = (df.blueTeamAssists * df.blueTeamKills) - (df.redTeamAssists * df.redTeamKills)
    df2['blueTeamJungleMonstersKilledDiff'] = (
            df.blueTeamTotalJungleMonstersKilled - df.redTeamTotalJungleMonstersKilled)
    df2['blueTeamMinionsKilledDiff'] = (df.blueTeamTotalMinionsKilled - df.redTeamTotalMinionsKilled)
    df2['blueTeamAvgLevelDiff'] = (df.blueTeamAvgLevel - df.redTeamAvgLevel)
    df2['blueTeamCsPerMinuteDiff'] = (df.blueTeamCsPerMinute - df.redTeamCsPerMinute)
    df2['blueTeamGoldPerMinuteDiff'] = (df.blueTeamGoldPerMinute - df.redTeamGoldPerMinute)
    df2['blueTeamTowersDestroyedDiff'] = (df.blueTeamTowersDestroyed - df.redTeamTowersDestroyed)
    df2['blueTeamDragonsKilledDiff'] = (df.blueTeamDragonsKilled - df.redTeamDragonsKilled)
    df2['blueTeamHeraldsKilledDiff'] = (df.blueTeamHeraldsKilled - df.redTeamHeraldsKilled)
    df2['blueTeamVoidGrubsKilledDiff'] = (df.blueTeamVoidGrubsKilled - df.redTeamVoidGrubsKilled)
    df2['blueTeamWin'] = df.blueTeamWin
    df2.to_csv(f'{output_location}/prepared_data.csv', index=False)

    df_train_val = df2.sample(frac=0.9, random_state=777)
    df_test = df2.drop(df_train_val.index)

    df_val = df_train_val.sample(frac=0.15, random_state=777)
    df_train = df_train_val.drop(df_val.index)

    df_train.to_csv(f'{output_location}/prepared_data_train.csv', index=False)
    df_val.to_csv(f'{output_location}/prepared_data_val.csv', index=False)
    df_test.to_csv(f'{output_location}/prepared_data_test.csv', index=False)
