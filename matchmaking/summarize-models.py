import argparse
import numpy as np
import pandas as pd
import pickle


def read_pickle(handle):
    return pickle.load(open(handle, "rb"))


def write_file(dataframe, handle):
    dataframe.to_csv(handle, sep='\t', index=False)


def compare_all_models(models_dictionary):
    all_models = list(models_dictionary.keys())
    df = pd.DataFrame(0, index=all_models, columns=all_models)
    for model_row in all_models:
        for model_col in all_models:
            case_model = models_dictionary[model_row]
            comparison_model = models_dictionary[model_col]

            delta_mAP, series = compare_two_models(case_model, comparison_model, 10000)
            series_value_counts = series.abs().ge(abs(delta_mAP)).value_counts()
            if True in series_value_counts.index:
                pvalue = series_value_counts[True] / series.shape[0]
            else:
                pvalue = 0

            df.loc[model_row, model_col] = pvalue
    return df


def compare_two_models(case_dict, comparison_dict, N):
    case_mAP = case_dict['mean_average_precision']
    comparison_mAP = comparison_dict['mean_average_precision']
    delta_mAP = case_mAP - comparison_mAP

    aps = pd.concat([
        case_dict['average_precision'].rename('case'),
        comparison_dict['average_precision'].rename('comparison')
    ], axis=1)
    aps['shuffle_case'] = 0
    aps['shuffle_comparison'] = 0

    delta_mAPs = pd.Series(index=range(0, N), dtype=float)
    for seed in delta_mAPs.index:
        rng = np.random.default_rng(seed=seed)
        aps['rng'] = rng.binomial(1, 0.5, aps.shape[0])

        aps.loc[aps['rng'].eq(1), 'shuffle_case'] = aps.loc[aps['rng'].eq(1), 'case']
        aps.loc[aps['rng'].eq(1), 'shuffle_comparison'] = aps.loc[aps['rng'].eq(1), 'comparison']
        aps.loc[aps['rng'].eq(0), 'shuffle_case'] = aps.loc[aps['rng'].eq(0), 'case']
        aps.loc[aps['rng'].eq(0), 'shuffle_comparison'] = aps.loc[aps['rng'].eq(0), 'comparison']

        shuffled_case_mAP = aps['shuffle_case'].mean()
        shuffled_comparison_mAP = aps['shuffle_comparison'].mean()
        shuffled_delta_mAP = shuffled_case_mAP - shuffled_comparison_mAP
        delta_mAPs.loc[seed] = shuffled_delta_mAP
    return delta_mAP, delta_mAPs


def summarize_models(db):
    columns = ['model_name',
               'mean_average_precision',
               'average_precision_at_k=1',
               'average_precision_at_k=2',
               'average_precision_at_k=3',
               'average_precision_at_k=4',
               'average_precision_at_k=5',
               'description']

    list_of_series = []
    for model in db.keys():
        series = pd.Series(pd.NA, name=model, index=columns)
        series.loc['model_name'] = model
        series.loc['mean_average_precision'] = db[model]['mean_average_precision']
        for k in range(1, 6):
            series.loc['average_precision_at_k={}'.format(k)] = db[model]['ap@k'][k]
        series.loc['description'] = db[model]['description']
        list_of_series.append(series.to_frame().T)
    df = pd.concat(list_of_series, ignore_index=True)
    return df.sort_values(['average_precision_at_k=1', 'mean_average_precision'], ascending=False)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(prog='Summarize models',
                                         description='Creates summary output and compares models')
    arg_parser.add_argument('--input', '-i',
                            help='models.evaluated.pkl file',
                            default='outputs/models.evaluated.pkl')
    arg_parser.add_argument('--output_directory', '-o',
                            help='output path to write outputs to',
                            default='outputs')
    args = arg_parser.parse_args()

    models = read_pickle(args.input)
    summary = summarize_models(models)
    write_file(summary, f"{args.output_directory}/models.summary.txt")

    model_pairwise_comparison = compare_all_models(models)
    write_file(model_pairwise_comparison, f"{args.output_directory}/models.pairwise-comparison.txt")
