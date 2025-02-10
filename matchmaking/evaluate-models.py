import argparse
import numpy as np
import os
import pandas as pd
import pickle
import subprocess

from metrics import Metrics
from plots import AveragePrecision, AveragePrecisionK

SEED = 42
CASE = 'case'
COMPARISON = 'comparison'
INTERSECTION = 'labels_intersection'
N_INTERSECTION = 'labels_n_intersection'
SAMPLE_NAME = 'sample_name'


def merge_dataframes(left_dataframe, right_dataframe, on_columns, how='left', set_index_to_on_columns=True):
    dataframe = pd.merge(left=left_dataframe, right=right_dataframe, on=on_columns, how=how)
    if set_index_to_on_columns:
        dataframe.set_index(on_columns, inplace=True)
    return dataframe


def read_models(list_of_files, measure='distance'):
    measures = ['distance', 'similarity']
    if measure not in measures:
        raise ValueError(f"Invalid measure. Expected one of: {', '.join(measures)}")

    dataframes = [pd.read_csv(handle, sep='\t').set_index(['case', 'comparison']) for handle in list_of_files]
    dataframe = pd.concat(dataframes, axis=1)

    if dataframe.columns.duplicated().sum() > 0:
        raise ValueError(f"Multiple columns of the same name observed: {', '.join(dataframe.columns)}")

    if measure == 'similarity':
        return pd.DataFrame(1, columns=dataframe.columns, index=dataframe.index).subtract(dataframe)
    else:
        return dataframe


def write_pickle(handle, output):
    file = open(handle, 'wb')
    pickle.dump(output, file)
    file.close()


def main(samples, distances, labels, output_directory, features=None, seed=42):
    np.random.seed(seed=seed)

    labeled = merge_dataframes(distances.reset_index(), labels.reset_index(), ['case', 'comparison'])
    if features:
        labeled = merge_dataframes(labeled.reset_index(), features.reset_index(), ['case', 'comparison'])

    model_names = distances.columns.tolist()
    model_descriptions = {}
    for model_name in model_names:
        model_descriptions[model_name] = ""

    evaluated_models_dictionary = Metrics.evaluate_models(samples, labeled, model_names, model_descriptions)
    write_pickle(
        handle=os.path.join(output_directory, 'models.evaluated.pkl'),
        output=evaluated_models_dictionary
    )
    AveragePrecision.plot(evaluated_models_dictionary, model_names, output_directory)
    AveragePrecisionK.plot(evaluated_models_dictionary, model_names, output_directory)

    for model_name in model_names:
        print(model_name)
        if features:
            output_columns = [
                'case', 'comparison',
                model_name, 'k', 'p@k', 'r@k', 'tps@k',
                'labels_n_intersection', 'labels_intersection', 'features_intersection',
                'labels_n_case', 'labels_unique_case', 'features_unique_case',
                'labels_n_comparison', 'labels_unique_comparison', 'features_unique_comparison'
            ]
        else:
            output_columns = [
                'case', 'comparison',
                model_name, 'k', 'p@k', 'r@k', 'tps@k',
                'labels_n_intersection', 'labels_intersection',
                'labels_n_case', 'labels_unique_case',
                'labels_n_comparison', 'labels_unique_comparison'
            ]

        df = evaluated_models_dictionary[model_name]['calculated']
        (
            df
            .reset_index()
            .loc[:, output_columns]
            .to_csv(
                os.path.join(output_directory, 'models', f'{model_name}.fully_annotated.result.txt'),
                sep='\t',
                index=False
            )
        )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Evaluate distances',
                                         description='Evaluate model distances')
    arg_parser.add_argument('--distance', '-d', action="append", help="Distance models, closer to zero = more similar")
    arg_parser.add_argument('--affinity', '-a', action="append", help="Affinity models, closer to one = more similar")
    arg_parser.add_argument('--labels', '-l', required=True, help='pairwise comparison of labels')
    arg_parser.add_argument('--features', '-f', required=False, help='pairwise comparison of features')
    arg_parser.add_argument('--samples', '-s', required=True, help='list of all samples considered')
    arg_parser.add_argument('--output-directory', '-o', default='output', help='Output directory')
    args = arg_parser.parse_args()

    output_directory = args.output_directory
    subprocess.call(f"mkdir -p {output_directory}", shell=True)
    subprocess.call(f"mkdir -p {output_directory}/distances", shell=True)
    subprocess.call(f"mkdir -p {output_directory}/features", shell=True)
    subprocess.call(f"mkdir -p {output_directory}/img", shell=True)
    subprocess.call(f"mkdir -p {output_directory}/models", shell=True)

    samples_list = pd.read_csv(args.samples, sep='\t', usecols=['sample_name']).loc[:, 'sample_name'].tolist()

    models = []
    if args.distance:
        distance_models = read_models(args.distance, measure='distance')
        models.append(distance_models)
    if args.affinity:
        similarity_models = read_models(args.affinity, measure='similarity')
        models.append(similarity_models)
    model_results = pd.concat(models, axis=1)

    sample_labels = pd.read_csv(args.labels, sep='\t').set_index(['case', 'comparison'])
    if args.features:
        sample_features = pd.read_csv(args.features, sep='\t').set_index(['case', 'comparison'])
        main(samples_list, model_results, sample_labels, output_directory, features=sample_features)
    else:
        main(samples_list, model_results, sample_labels, output_directory)
