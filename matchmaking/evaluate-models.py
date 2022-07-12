import argparse
import numpy as np
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


def write_pickle(handle, output):
    file = open(handle, 'wb')
    pickle.dump(output, file)
    file.close()


def main(samples, distances, labels, output_directory, features=None, seed=42):
    np.random.seed(seed=seed)

    labeled = pd.concat([distances, labels], axis=1)
    if features:
        labeled = pd.concat([labeled, features], axis=1)

    model_names = distances.columns.tolist()
    model_descriptions = {}
    for model_name in model_names:
        model_descriptions[model_name] = ""

    evaluated_models_dictionary = Metrics.evaluate_models(samples, labeled, model_names, model_descriptions)
    write_pickle(f'{output_directory}/models.evaluated.pkl', evaluated_models_dictionary)
    AveragePrecision.plot(evaluated_models_dictionary, model_names, output_directory)
    AveragePrecisionK.plot(evaluated_models_dictionary, model_names, output_directory)

    for model_name in model_names:
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
        (df
         .reset_index()
         .loc[:, output_columns]
         .to_csv(f'{output_directory}/models/{model_name}.fully_annotated.result.txt', sep='\t')
         )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Evaluate distances',
                                         description='Evaluate model distances')
    arg_parser.add_argument('--distance', '-d', action="append", help="Distance files")
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

    handles = args.distance
    samples = pd.read_csv(args.samples, sep='\t', usecols=['sample_name']).loc[:, 'sample_name'].tolist()
    df = pd.concat([pd.read_csv(handle, sep='\t', index_col=[0]).set_index(['case', 'comparison']) for handle in handles], axis=1)
    labels = pd.read_csv(args.labels, sep='\t').set_index(['case', 'comparison'])
    if args.features:
        features = pd.read_csv(args.features, sep='\t').set_index(['case', 'comparison'])
        main(samples, df, labels, output_directory, features=features)
    else:
        main(samples, df, labels, output_directory)
