# Matchmaking inputs
To run matchmaking, the following inputs must be configured for your cohort:
- `somatic_variants`
- `copy_number_alterations`
- `fusions`
- `samples`
- `labeled samples`

A pairwise comparison must also be performed on samples and their labels. Please follow the following steps to configure your inputs to run matchmaking,
1. Follow instructions under [`formatted/`](formatted/) to format your samples and molecular features
2. Follow instructions under [`annotated/`](annotated/) to annotate molecular features after formatting
3. Follow instructions under [`pairwise-comparisons/`](pairwise-comparisons/) to perform pairwise comparisons of both labels and molecular features, after annotating molecular features

Files utilized for the present study in the `formatted/` and `annotated/` are committed to Github. With `pairwise-comparisons/`, `pairwise-comparisons/samples.pairwise-labels.txt` is as utilized in the present study but the file generated for the molecular feature comparison for the present study is ~450 MB. As Github has a file size limit of 100 MB, a smaller version of this file has been committed to Github by taking the top 50 rows of the actual output. Follow the instructions under `pairwise-comparison/` to regenerate the file locally. 

The [`datasources/`](datasources/) folder contains back ups of MOAlmanac and CGC, as used in the present study.
