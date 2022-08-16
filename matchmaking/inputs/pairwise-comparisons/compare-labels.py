import argparse
import pandas as pd

SAMPLE_COLUMN = "sample_name"
CASE = "case"
COMPARISON = "comparison"
N_CASE = "labels_n_case"
N_COMPARISON = "labels_n_comparison"
N_INTERSECTION = "labels_n_intersection"
CASE_UNIQUE = "labels_unique_case"
COMPARISON_UNIQUE = "labels_unique_comparison"
INTERSECTION = "labels_intersection"

COLUMNS = [CASE, COMPARISON, N_CASE, N_COMPARISON, N_INTERSECTION, CASE_UNIQUE, COMPARISON_UNIQUE, INTERSECTION]


def calculate_upper_bound(total_samples, df):
    n_samples = df[~df[N_INTERSECTION].eq(0)][CASE].drop_duplicates().shape[0]
    pct_samples = round(100 * (total_samples / n_samples), 2)
    return n_samples, pct_samples


def import_samples(handle, **kwargs):
    dataframe = read_tsv(handle, **kwargs)
    return dataframe[SAMPLE_COLUMN].astype(str).tolist()


def list_difference(list1, list2):
    return [value for value in list1 if value not in list2]


def list_intersection(list1, list2):
    return [value for value in list1 if value in list2]


def subset_by_samples(data_dataframe, samples_list):
    dataframe = data_dataframe[data_dataframe[SAMPLE_COLUMN].isin(samples_list)]
    return dataframe.reset_index(drop=True)


def read_tsv(handle, **kwargs):
    return pd.read_csv(handle, sep='\t', **kwargs)


def write_data(dataframe, handle):
    dataframe.to_csv(handle, sep='\t', index=False)


def compare(samples, dataframe, comparison_column, display_columns):
    results = []
    for case in samples:
        for comparison in samples:
            case_group = dataframe[dataframe[SAMPLE_COLUMN].eq(case)]
            comparison_group = dataframe[dataframe[SAMPLE_COLUMN].eq(comparison)]
            case_values = case_group[comparison_column].drop_duplicates().tolist()
            comparison_values = comparison_group[comparison_column].drop_duplicates().tolist()
            intersection = list_intersection(case_values, comparison_values)
            case_unique_values = list_difference(case_values, comparison_values)
            comparison_unique_values = list_difference(comparison_values, case_values)
            result = (case,
                      comparison,
                      case_group.shape[0],
                      comparison_group.shape[0],
                      len(intersection),
                      ', '.join(case_unique_values),
                      ', '.join(comparison_unique_values),
                      ', '.join(intersection)
                      )
            results.append(result)

    return pd.DataFrame(results, columns=display_columns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Pairwise compare therapies",
                                     description="Perform pairwise comparison of samples to identify overlap")
    parser.add_argument('--input', '-i', required=True, help="input file")
    parser.add_argument('--column', '-c', required=True, default='therapy_name', help='column with comparison values')
    parser.add_argument('--samples', '-s', required=True, help='dataframe of sample names, will subset if passed')
    parser.add_argument('--output', '-o', required=False, default="samples.pairwise-labels.txt", help="output name")
    args = parser.parse_args()

    data = read_tsv(args.input, usecols=[SAMPLE_COLUMN, args.column])
    all_samples = import_samples(args.samples)
    data = subset_by_samples(data, all_samples)
    data['sample_name'] = data['sample_name'].astype(str)

    compared_data = compare(all_samples, data, args.column, COLUMNS)
    write_data(compared_data, args.output)

    n, pct = calculate_upper_bound(len(all_samples), compared_data)
    print(f"Of {len(all_samples)} samples considered, {pct}% ({n}) share a label with at least one other sample")
