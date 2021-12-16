import argparse
import numpy as np
import pandas as pd
import pickle

import models as models
from metrics import Metrics
from plots import AveragePrecision, AveragePrecisionK

SEED = 42
CASE = 'case'
COMPARISON = 'comparison'
INTERSECTION = 'intersection'
N_INTERSECTION = 'n_intersection'
N_SHARED = 'n_shared'
SAMPLE_NAME = 'sample_name'


def format_pairs(dataframe):
    return (
        dataframe
            .sort_values([CASE, COMPARISON], ascending=[True, False])
            .set_index([CASE, COMPARISON]).rename(columns={N_INTERSECTION: N_SHARED})
            .loc[:, N_SHARED]
    )


def preallocate_column(df, column, value):
    df[column] = value
    return df


def write_pickle(handle, output):
    file = open(handle, 'wb')
    pickle.dump(output, file)
    file.close()


def main(inputs, samples):
    np.random.seed(seed=42)

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

    calculated = [model.calculate(inputs, samples) for model in models_list]
    model_names = [model.label for model in models_list]
    model_descriptions = {}
    for model in models_list:
        model_descriptions[model.label] = model.description

    distances = pd.concat(calculated, axis=1)
    labels = format_pairs(inputs['pairwise'])

    distances.loc[distances.index, N_SHARED] = labels.loc[distances.index]
    labeled = distances
    labeled.to_csv('outputs/models.labeled.txt', sep='\t')

    evaluated_models_dictionary = Metrics.evaluate_models(samples, labeled, model_names, model_descriptions)
    write_pickle('outputs/models.evaluated.pkl', evaluated_models_dictionary)
    AveragePrecision.plot(evaluated_models_dictionary, model_names)
    AveragePrecisionK.plot(evaluated_models_dictionary, model_names)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Matchmaking',
                                         description='Perform profile-to-profile matchmaking')
    arg_parser.add_argument('--variants', '-v',
                            help='File handle to annotated somatic variants',
                            default='inputs/annotated/samples.variants.annotated.txt')
    arg_parser.add_argument('--copy_number_alterations', '-cn',
                            help='File handle to annotated copy number alterations',
                            default='inputs/annotated/samples.copy_numbers.annotated.txt')
    arg_parser.add_argument('--fusions', '-f',
                            help='File handle to annotated fusions',
                            default='inputs/annotated/samples.fusions.annotated.txt')
    arg_parser.add_argument('--fusions_gene1', '-f1',
                            help='File handle to annotated fusions, just gene1',
                            default='inputs/annotated/samples.fusions.annotated.gene1.txt')
    arg_parser.add_argument('--fusions_gene2', '-f2',
                            help='File handle to annotated fusions, just gene2',
                            default='inputs/annotated/samples.fusions.annotated.gene2.txt')
    arg_parser.add_argument('--samples', '-s',
                            help='File handle to sample information and which samples to use',
                            default='inputs/formatted/samples.summary.txt')
    arg_parser.add_argument('--labels', '-l',
                            help='File handle sample labels',
                            default='inputs/formatted/samples.sensitive_therapies.txt')
    arg_parser.add_argument('--pairwise', '-p',
                            help='File handle sample label pairwise comparisons',
                            default='inputs/formatted/samples.pairwise.txt')
    arg_parser.add_argument('--almanac', '-a',
                            help='File handle to molecular oncology almanac',
                            default='inputs/datasources/moalmanac.json')
    arg_parser.add_argument('--cgc', '-c',
                            help='File handle to cancer gene census',
                            default='inputs/datasources/cancer_gene_census_v85.tsv')
    args = arg_parser.parse_args()

    input_handles = {
        'variants': args.variants,
        'copy_number_alterations': args.copy_number_alterations,
        'fusions': args.fusions,
        'fusions_gene1': args.fusions_gene1,
        'fusions_gene2': args.fusions_gene2,
        'samples': args.samples,
        'labels': args.labels,
        'pairwise': args.pairwise,
        'almanac': args.almanac,
        'cgc': args.cgc
    }

    inputs_dictionary = {}
    feature_data_types = ['variants', 'copy_number_alterations', 'fusions', 'fusions_gene1', 'fusions_gene2']
    flat_data_structures = feature_data_types + ['samples', 'labels', 'pairwise', 'cgc']
    for data_type in flat_data_structures:
        inputs_dictionary[data_type] = pd.read_csv(input_handles[data_type], sep='\t')
    inputs_dictionary['almanac'] = input_handles['almanac']

    samples_to_use = inputs_dictionary['samples'][SAMPLE_NAME].tolist()
    for data_type in feature_data_types:
        dataframe = inputs_dictionary[data_type]
        dataframe = dataframe[dataframe[SAMPLE_NAME].isin(samples_to_use)]
        inputs_dictionary[data_type] = dataframe

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

    main(inputs_dictionary, samples_to_use)
