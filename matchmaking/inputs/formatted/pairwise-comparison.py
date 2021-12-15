import argparse
import pandas as pd

SAMPLE_COLUMN = "sample_name"
CASE = "case"
COMPARISON = "comparison"
N_CASE = "n_case"
N_COMPARISON = "n_comparison"
N_INTERSECTION = "n_intersection"
INTERSECTION = "intersection"

COLUMNS = [CASE, COMPARISON, N_CASE, N_COMPARISON, N_INTERSECTION, INTERSECTION]


def import_samples(handle, **kwargs):
    dataframe = read_tsv(handle, **kwargs)
    return dataframe[SAMPLE_COLUMN].tolist()


def list_intersection(list1, list2):
    return [value for value in list1 if value in list2]


def subset_by_samples(data_dataframe, samples_list):
    dataframe = data_dataframe[data_dataframe[SAMPLE_COLUMN].isin(samples_list)]
    return dataframe.reset_index(drop=True)


def read_tsv(handle, **kwargs):
    return pd.read_csv(handle, sep='\t', **kwargs)


def write_data(dataframe, handle):
    dataframe.to_csv(handle, sep='\t', index=False)


def compare(samples, dataframe, comparison_column):
    results = []
    for case in samples:
        for comparison in samples:
            case_group = dataframe[dataframe[SAMPLE_COLUMN].eq(case)]
            comparison_group = dataframe[dataframe[SAMPLE_COLUMN].eq(comparison)]
            case_values = case_group[comparison_column].tolist()
            comparison_values = comparison_group[comparison_column].tolist()
            intersection = list_intersection(case_values, comparison_values)
            intersection_string = ', '.join(intersection)
            result = (case,
                      comparison,
                      case_group.shape[0],
                      comparison_group.shape[0],
                      len(intersection),
                      intersection_string
                      )
            results.append(result)

    return pd.DataFrame(results, columns=COLUMNS)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Pairwise compare therapies",
                                     description="Perform pairwise comparison of samples to identify overlap")
    parser.add_argument('--input', '-i', required=True, help="input file")
    parser.add_argument('--column', '-c', required=True, default='therapy_name', help='column with comparison values')
    parser.add_argument('--samples', '-s', required=True, help='dataframe of sample names, will subset if passed')
    parser.add_argument('--output', '-o', required=False, default="samples.pairwise.txt", help="output name")
    args = parser.parse_args()

    data = read_tsv(args.input, usecols=[SAMPLE_COLUMN, args.column])
    all_samples = import_samples(args.samples)
    data = subset_by_samples(data, all_samples)

    compared_data = compare(all_samples, data, args.column)
    write_data(compared_data, args.output)
