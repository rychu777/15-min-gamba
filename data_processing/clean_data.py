import pandas as pd


def data_to_final(input_file: str, output_file: str) -> None:
    """
    Cleans and processes the input data stored in Feather format and saves the cleaned data to a new Feather file.

    Args:
    :argument: input_file (str): The path to the input Feather file containing the raw data.
    :argument: output_file (str): The path to save the cleaned data as a new Feather file.

    Returns:
    :return: None: This function does not return anything. It reads the input data from the specified Feather file,
              performs data cleaning operations (removing incorrect values, duplicates, and outliers),
              and saves the cleaned data to the specified location.
    """
    df = pd.read_feather(input_file)
    df = df[df.blueTeamWin != 2]  # Removing data containing incorrect values
    df = df.drop_duplicates()  # Removing duplicates in case there still are some
    df = df[df.gameDuration < 6000]  # Getting rid of all games longer than 100 minutes
    df = df[df.blueTeamGoldPerMinute != 0]  # Removing data containing incorrect values
    df = df[df.redTeamGoldPerMinute != 0]  # Removing data containing incorrect values
    df = df.reset_index(drop=True)  # Resets index, argument is to prevent pandas to create another index column
    df.to_feather(output_file)  # Ended up with 41 282 correct match data
