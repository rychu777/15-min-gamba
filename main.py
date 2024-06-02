from back_end.change_format import *
from back_end.feature_engineering import prepare_data
from back_end.building_the_model import *


def main() -> None:
    summoner_ids_file = 'test_summoner_ids.txt'
    puuids_file = 'test_puuids.txt'
    match_ids_file = 'Data_initial/unique_match_ids_part_4.txt'
    csv_data_file = 'Data_initial/match_data.csv'
    feather_data_file = 'Data_initial/match_data.feather'
    final_data_file = 'Data/final_data.feather'
    preview_csv_file = 'Data_initial/preview_data.csv'
    prepared_data_location = 'Data'
    Key = 'RIOT_API_KEY'
    tier = 'CHALLENGER'
    min_summoners = 150

    #  gather_summoner_ids(API_key=Key, output_file=summoner_ids_file, tier=tier, min_players=min_summoners)
    #  extract_puuids(API_key=Key, input_file=summoner_ids_file, output_file=puuids_file)
    #  fetch_match_ids(API_key=Key, input_file=puuids_file, output_file=match_ids_file)
    #  remove_duplicates(match_ids_file)
    #  get_match_data(API_key=Key, input_file=match_ids_file, output_file=csv_data_file)
    #  csv_to_feather(csv_data_file, feather_data_file)
    #  data_to_final(feather_data_file, final_data_file)
    #  feather_to_csv(final_data_file, preview_csv_file)

    #  analyzer = DataAnalyzer(final_data_file)
    #  analyzer.winrate()
    #  analyzer.winrate_per_first_blood()
    #  analyzer.gold_and_cs()
    #  analyzer.heatmap()
    #  analyzer.multicollinearity()

    #  prepare_data(final_data_file, prepared_data_location)
    #  remove_column_names('Data/prepared_data_test.csv', 'Data/prepared_data_test.csv')
    #  remove_column_names('Data/prepared_data_train.csv', 'Data/prepared_data_train.csv')
    #  remove_column_names('Data/prepared_data_val.csv', 'Data/prepared_data_val.csv')

    classifier = NeuralNetworkClassifier('Data/prepared_data_train.csv',
                                         'Data/prepared_data_test.csv',
                                         'Data/prepared_data_val.csv')

    # Train the model
    classifier.train()

    # Make predictions
    predictions = classifier.predict()

    # Evaluate model performance
    accuracy, precision, recall, f1, conf_matrix = classifier.evaluate(predictions)

    # Plot ROC curve
    classifier.plot_roc_curve(predictions)

    # Print additional evaluation metrics
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("Confusion Matrix:\n", conf_matrix)
    print(conf_matrix[0][0])
    print(conf_matrix[0][1])
    print(conf_matrix[1][0])
    print(conf_matrix[1][1])


if __name__ == '__main__':
    main()
