import pandas as pd


def csv_to_feather(input_file: str, output_file: str) -> None:
    """
    Converts a CSV file to the Feather format.

    Args:
    :argument: input_file (str): The path to the input CSV file.
    :argument: output_file (str): The path to save the output Feather file.

    Returns:
    :argument: None: This function does not return anything. It converts the CSV file to Feather format
              and saves it to the specified location.
    """
    df = pd.read_csv(input_file)
    df.to_feather(output_file)


def feather_to_csv(input_file: str, output_file: str) -> None:
    """
    Converts a Feather file to a CSV file.

    Args:
    :argument: input_file (str): The path to the input Feather file.
    :argument: output_file (str): The path to save the output CSV file.

    Returns:
    :return: None: This function does not return anything. It reads the data from the input Feather file,
            converts it to CSV format, and saves it to the specified location.
    """
    df = pd.read_feather(input_file)
    df.to_csv(output_file)


def remove_duplicates(input_file: str, output_file: str) -> None:
    """
    Remove duplicates from a text file.

    Args:
    input_file (str): Path to the input file containing lines of code.
    output_file (str): Path to the output file to write unique lines.

    Returns:
    None
    """
    unique_lines = set()

    with open(input_file, 'r') as f:
        for line in f:
            unique_lines.add(line.strip())

    with open(output_file, 'w') as f:
        for line in unique_lines:
            f.write(line + '\n')


def remove_column_names(input_file: str) -> None:
    """
    Removes the first row of data from a CSV file.

    :param input_file: Path to the input CSV file.
    :return: None
    """

    df = pd.read_csv(input_file, skiprows=1)

    df.to_csv(input_file, index=False)
