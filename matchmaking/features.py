
class Features:
    case = 'case'
    comparison = 'comparison'
    features_intersection = "features_intersection"
    features_unique_case = "features_unique_case"
    features_unique_comparison = "features_unique_comparison"
    sample_name = "sample_name"

    @classmethod
    def compare_pairwise(cls, variants, copy_number_alterations, fusions, samples, pairwise, subset=False):
        if subset:
            variants = cls.subset_dataframe(variants)
            copy_number_alterations = cls.subset_dataframe(copy_number_alterations)
            fusions = cls.subset_dataframe(fusions)
        variants_dict = cls.generate_features_list(samples, variants, cls.format_variant_strings)
        copy_numbers_dict = cls.generate_features_list(samples, copy_number_alterations, cls.format_copy_number_string)
        fusions_dict = cls.generate_features_list(samples, fusions, cls.format_fusion_string)

        dataframe = pairwise.loc[:, ['case', 'comparison']]

        for index in pairwise.index:
            case = pairwise.loc[index, cls.case]
            comparison = pairwise.loc[index, cls.comparison]

            case_features = variants_dict[case] + copy_numbers_dict[case] + fusions_dict[case]
            comparison_features = variants_dict[comparison] + copy_numbers_dict[comparison] + fusions_dict[comparison]
            features_intersection = cls.list_intersection(case_features, comparison_features)
            features_unique_case = cls.list_difference(case_features, comparison_features)
            features_unique_comparison = cls.list_difference(comparison_features, case_features)

            dataframe.loc[index, cls.features_intersection] = ', '.join(features_intersection)
            dataframe.loc[index, cls.features_unique_case] = ', '.join(features_unique_case)
            dataframe.loc[index, cls.features_unique_comparison] = ', '.join(features_unique_comparison)
        return dataframe.set_index([cls.case, cls.comparison])

    @staticmethod
    def format_copy_number_string(row):
        return ' '.join([row['feature'], row['alteration_type']])

    @staticmethod
    def format_fusion_string(row):
        return '--'.join([row['feature'], row['partner']])

    @staticmethod
    def format_variant_strings(row):
        return ' '.join([row['feature'], row['alteration']]
                        if row['alteration_type'] != 'Splice Site'
                        else [row['feature'], row['alteration_type']]
                        )

    @classmethod
    def generate_features_list(cls, samples, dataframe, row_function):
        dictionary = {}
        for sample in samples:
            dictionary[sample] = []
        for label, group in dataframe.groupby(cls.sample_name):
            features_list = (group
                             .fillna('')
                             .apply(lambda row: row_function(row), axis=1)
                             .tolist()
                             )
            dictionary[label] = features_list
        return dictionary

    @staticmethod
    def list_intersection(list1, list2):
        return sorted([value for value in list1 if value in list2])

    @staticmethod
    def list_difference(list1, list2):
        return sorted([value for value in list1 if value not in list2])

    @staticmethod
    def subset_dataframe(dataframe):
        idx = ~dataframe['feature_match_1'].eq(0) | dataframe['cgc_bin'].eq(1)
        return dataframe[idx].reset_index()
