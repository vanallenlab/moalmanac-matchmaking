import argparse
import json
import numpy as np
import os
import pandas as pd
import pickle

import models as models
from metrics import Metrics
from plots import AveragePrecision, AveragePrecisionK

SEED = 42
CASE = 'case'
COMPARISON = 'comparison'
INTERSECTION = 'labels_intersection'
N_INTERSECTION = 'labels_n_intersection'
SAMPLE_NAME = 'sample_name'


def preallocate_column(df, column, value):
    df[column] = value
    return df


def read_json(handle):
    with open(handle) as file:
        return json.load(file)


def write_pickle(handle, output):
    file = open(handle, 'wb')
    pickle.dump(output, file)
    file.close()


def main(inputs, samples, seed=SEED, output_directory="outputs"):
    np.random.seed(seed=seed)

    models_list = [
        models.AlmanacGenes,
        models.AlmanacFeatureTypes,
        models.AlmanacFeatures,
        models.CGC,
        models.CGCFeatureTypes,
        #models.Compatibility,
        models.NonsynVariantCount,
        models.PCAonAlmanac,
        models.PCAonCGC,
        models.RankedSortAlmanacEvidenceCGC,
        models.SNFbyEvidenceCGC,
        models.SNFTypesCGC,
        models.SNFTypesCGCwithEvidence,
        models.SNFTypesAlmanac,
        models.Tree
    ]

    calculated = [model.calculate(inputs, samples, output_directory) for model in models_list]
    model_names = [model.label for model in models_list]
    model_descriptions = {}
    for model in models_list:
        model_descriptions[model.label] = model.description

    distances = pd.concat(calculated, axis=1)
    labeled = pd.concat([distances, inputs['labels'], inputs['features']], axis=1)

    evaluated_models_dictionary = Metrics.evaluate_models(samples, labeled, model_names, model_descriptions)
    write_pickle(
        handle=os.path.join(output_directory, 'models.evaluated.pkl'),
        output=evaluated_models_dictionary
    )
    AveragePrecision.plot(evaluated_models_dictionary, model_names, output_directory)
    AveragePrecisionK.plot(evaluated_models_dictionary, model_names, output_directory)

    for model in models_list:
        output_columns = [
            'case', 'comparison',
            model.label, 'k', 'p@k', 'r@k', 'tps@k',
            'labels_n_intersection', 'labels_intersection', 'features_intersection',
            'labels_n_case', 'labels_unique_case', 'features_unique_case',
            'labels_n_comparison', 'labels_unique_comparison', 'features_unique_comparison'
        ]

        df = evaluated_models_dictionary[model.label]['calculated']
        (
            df
            .reset_index()
            .loc[:, output_columns]
            .to_csv(
                os.path.join(output_directory, 'models', f'{model.label}.fully_annotated.result.txt'),
                sep='\t'
            )
        )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Matchmaking',
                                         description='Perform profile-to-profile matchmaking')
    arg_parser.add_argument('--config', '-c',
                            help='File handle to input configuration',
                            default='config.default.json')
    args = arg_parser.parse_args()

    config = read_json(args.config)
    input_handles = {
        'variants': config['variants']['handle'],
        'copy_number_alterations': config['copy_number_alterations']['handle'],
        'fusions': config['fusions']['handle'],
        'fusions_gene1': config['fusions-gene1']['handle'],
        'fusions_gene2': config['fusions-gene2']['handle'],
        'samples': config['samples']['handle'],
        'features': config['features']['handle'],
        'labels': config['labels']['handle'],
        'almanac': config['datasources']['moalmanac'],
        'cgc': config['datasources']['cgc'],
        'output_directory': config['output_directory']
    }

    inputs_dictionary = {}
    feature_data_types = ['variants', 'copy_number_alterations', 'fusions', 'fusions_gene1', 'fusions_gene2']
    flat_data_structures = feature_data_types + ['samples', 'labels', 'features', 'cgc']
    for data_type in flat_data_structures:
        inputs_dictionary[data_type] = pd.read_csv(input_handles[data_type], sep='\t')
    inputs_dictionary['almanac'] = input_handles['almanac']

    samples_to_use = inputs_dictionary['samples'][SAMPLE_NAME].astype(str).tolist()
    for data_type in feature_data_types:
        dataframe = inputs_dictionary[data_type]
        dataframe[SAMPLE_NAME] = dataframe[SAMPLE_NAME].astype(str)
        dataframe = dataframe[dataframe[SAMPLE_NAME].isin(samples_to_use)]
        inputs_dictionary[data_type] = dataframe
    for data_type in ['labels', 'features']:
        dataframe = inputs_dictionary[data_type]
        dataframe[CASE] = dataframe[CASE].astype(str)
        dataframe[COMPARISON] = dataframe[COMPARISON].astype(str)
        dataframe = dataframe[dataframe[CASE].isin(samples_to_use) & dataframe[COMPARISON].isin(samples_to_use)]
        inputs_dictionary[data_type] = (dataframe
                                        .sort_values([CASE, COMPARISON], ascending=True)
                                        .set_index([CASE, COMPARISON]))

    inputs_dictionary['variants'] = preallocate_column(inputs_dictionary['variants'],
                                                       'feature_type',
                                                       models.Models.variant)
    inputs_dictionary['copy_number_alterations'] = preallocate_column(inputs_dictionary['copy_number_alterations'],
                                                                      'feature_type',
                                                                      models.Models.copy_number)
    inputs_dictionary['copy_number_alterations'] = preallocate_column(inputs_dictionary['copy_number_alterations'],
                                                                      'alteration',
                                                                      '')
    for data_type in ['fusions', 'fusions_gene1', 'fusions_gene2']:
        dataframe = inputs_dictionary[data_type]
        dataframe = preallocate_column(dataframe, 'feature_type', models.Models.rearrangement)
        dataframe = preallocate_column(dataframe, 'alteration_type', 'Fusion')
        inputs_dictionary[data_type] = dataframe

    output_directory = config['output_directory']
    os.makedirs(
        name=output_directory,
        exist_ok=True
    )
    os.makedirs(
        name=os.path.join(output_directory, 'distances'),
        exist_ok=True
    )
    os.makedirs(
        name=os.path.join(output_directory, 'features'),
        exist_ok=True
    )
    os.makedirs(
        name=os.path.join(output_directory, 'img'),
        exist_ok=True
    )
    os.makedirs(
        name=os.path.join(output_directory, 'models'),
        exist_ok=True
    )
    main(inputs=inputs_dictionary, samples=samples_to_use, output_directory=output_directory)
