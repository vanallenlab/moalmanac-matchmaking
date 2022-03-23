import argparse
import importlib
import pandas as pd

compare_labels = importlib.import_module("compare-labels")


SAMPLE_COLUMN = "sample_name"
CASE = "case"
COMPARISON = "comparison"
N_CASE = "features_n_case"
N_COMPARISON = "features_n_comparison"
N_INTERSECTION = "features_n_intersection"
CASE_UNIQUE = "features_unique_case"
COMPARISON_UNIQUE = "features_unique_comparison"
INTERSECTION = "features_intersection"


COLUMNS = [CASE, COMPARISON, N_CASE, N_COMPARISON, N_INTERSECTION, CASE_UNIQUE, COMPARISON_UNIQUE, INTERSECTION]


def format_feature_string(dataframe, format_function):
    dataframe["feature_string"] = dataframe.fillna("").apply(lambda row: format_function(row), axis=1)
    dataframe = dataframe[~dataframe["feature_string"].eq("")]
    return dataframe.loc[:, [SAMPLE_COLUMN, "feature_string"]]


def format_copy_number_string(row):
    return ' '.join([row['feature'], row['alteration_type']])


def format_fusion_string(row):
    return '--'.join([row['feature'], row['partner']])


def format_variant_strings(row):
    return ' '.join([row['feature'], row['alteration']]
                    if row['alteration_type'] != 'Splice Site'
                    else [row['feature'], row['alteration_type']]
                    )


def import_and_format_features(variants_handle, cnas_handle, fusions_handle, samples_list):
    variants = compare_labels.read_tsv(variants_handle) if variants_handle else pd.DataFrame()
    cnas = compare_labels.read_tsv(cnas_handle) if cnas_handle else pd.DataFrame()
    fusions = compare_labels.read_tsv(fusions_handle) if fusions_handle else pd.DataFrame()

    variants = subset_dataframe_by_samples(variants, samples_list)
    cnas = subset_dataframe_by_samples(cnas, samples_list)
    fusions = subset_dataframe_by_samples(fusions, samples_list)

    if args.subset_features:
        variants = subset_dataframe_by_databases(variants)
        cnas = subset_dataframe_by_databases(cnas)
        fusions = subset_dataframe_by_databases(fusions)

    variants = format_feature_string(variants, format_variant_strings) if not variants.empty else variants
    cnas = format_feature_string(cnas, format_copy_number_string) if not cnas.empty else cnas
    fusions = format_feature_string(fusions, format_fusion_string) if not fusions.empty else fusions
    return pd.concat([variants, cnas, fusions])


def subset_dataframe_by_databases(dataframe):
    idx = ~dataframe['feature_match_1'].eq(0) | dataframe['cgc_bin'].eq(1)
    return dataframe[idx].reset_index()


def subset_dataframe_by_samples(dataframe, samples):
    return dataframe[dataframe[SAMPLE_COLUMN].isin(samples)].reset_index(drop=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Compare molecular features pairwise",
                                     description="Perform pairwise comparison of samples to identify overlap")
    parser.add_argument('--case', help='Case sample name')
    parser.add_argument('--variants', '-v', required=False, help="Annotated somatic variants")
    parser.add_argument('--copy_number_alterations', '-c', required=False, help="Annotated copy number alterations")
    parser.add_argument('--fusions', '-f', required=False, help="Annotated fusions")
    parser.add_argument('--samples', '-s', required=True, help='dataframe of sample names, will subset if passed')
    parser.add_argument('--output', '-o', required=False, default="samples.pairwise-features.txt", help="output name")
    parser.add_argument('--subset_features', action="store_true",
                        help='Subset shown features to be genes in either MOAlmanac or Cancer Gene Census')
    args = parser.parse_args()

    all_samples = compare_labels.import_samples(args.samples)
    data = import_and_format_features(args.variants, args.copy_number_alterations, args.fusions, all_samples)
    data["sample_name"] = data["sample_name"].astype(str)

    compared_data = compare_labels.compare(all_samples, data, "feature_string", COLUMNS, args.case)
    compare_labels.write_data(compared_data, args.output)
