# Pairwise comparisons of features and labels
Pairwise comparisons to identify the intersection and difference of both labels _and_ molecular features for all sample pairs must be performed for use with matchmaking. While each model handles molecular features differently, the intersection and difference of molecular features for any given sample pair is reported. 

## Labels
A tab-delimited text file containing all pairwise comparisons of samples and noting the intersection and difference between labels should be produced. The script `compare-labels.py` can be used to perform this task. Pairwise comparisons of the same sample can either be kept or removed. To minimize the size of files present on Github, only the first 100 rows of the output are committed to this repository.

### Usage
Required arguments:
```bash
    --input, -i    <string> input file of labeled samples
    --column, -c   <string> column name of label in input
    --samples, -s  <string> file path to samples input to list all samples
```

Optional arguments:
```bash
    --output, -o    <string> output filename for pairwise comparisons (default: samples.pairwise-labels.txt)
```

Example:
```bash
python compare-labels.py -i ../formatted/samples.sensitive_therapies.txt -c therapy_name -s ../formatted/samples.summary.txt
```

### Output fields
The following column names will be present in the generated output,
- `case`, `sample_name` associated with case sample in the pairwise comparison
- `comparison`, `sample_name` associated with the comparison sample in the pairwise comparison
- `labels_n_case`, number of labels present in the labeled samples file for `case`
- `labels_n_comparison`, number of labels present in the labeled samples file for `comparison`
- `labels_n_intersection`, number of labels present in the labeled samples file for both `case` and `comparison`
- `labels_unique_case`, labels present in the labeled samples file for only `case`, delimited by `, `
- `labels_unique_comparison`, labels present in the labeled samples file for only `comparison`, delimited by `, `
- `labels_intersection`, labels present in the labeled samples file for both `case` and `comparison`, delimited by `, `

### Example output
| case | comparison | labels_n_case | labels_n_comparison | labels_n_intersection | labels_unique_case | labels_unique_comparison | labels_intersection | 
| -- | -- | -- | -- | -- | -- | -- | -- |
| A-001	| A-001 | 3 | 3 | 3 | | | AKT inhibitor VIII, Acetalax, rTRAIL |
| A-001 | A-002 | 3 | 1 | 0 | AKT inhibitor VIII, Acetalax, rTRAIL | Pemetrexed |  | 
| A-001 | A-010 | 3 | 2 | 1 | Acetalax, rTRAIL | Afatinib | AKT inhibitor VIII |

## Molecular features
A tab-delimited text file containing all pairwise comparisons of samples and noting the intersection and difference between molecular features should be produced. The script `compare-features.py` can be used to perform this task. Pairwise comparisons of the same sample can either be kept or removed.

### Usage
Required arguments:
```bash
    --input, -i    <string> input file of labeled samples
    --column, -c   <string> column name of label in input
    --samples, -s  <string> file path to samples input to list all samples
```

Optional arguments:
```bash
    --output, -o    <string> output filename for pairwise comparisons (default: samples.pairwise.txt)
```

Example:
```bash
python compare-labels.py -i samples.sensitive_therapies.txt -c therapy_name -s samples.summary.txt
```

### Output fields
The following column names will be present in the generated output,
- `case`, `sample_name` associated with case sample in the pairwise comparison
- `comparison`, `sample_name` associated with the comparison sample in the pairwise comparison
- `features_n_case`, number of features present in the `case` sample
- `features_n_comparison`, number of features present in the `comparison` sample
- `features_n_intersection`, number of features shared between the `case` and `comparison` samples
- `features_unique_case`, features present in the `case` sample that are _not_ present in the `comparison` sample, delimited by `, `
- `features_unique_comparison`, features present in the `comparison` sample that are _not_ present in the `case` sample, delimited by `, `
- `features_intersection`, features present in both the `case` and `comparison` samples, delimited by `, `

### Example output
| case | comparison | features_n_case | features_n_comparison | features_n_intersection | features_unique_case | features_unique_comparison | features_intersection | 
| -- | -- | -- | -- | -- | -- | -- | -- |
| A-001	| A-001 | 3 | 3 | 3 | | | BRAF p.V600E, CDKN2A Deletion, FLT3 Amplification |
| A-001 | A-002 | 3 | 1 | 0 | BRAF p.V600E, CDKN2A Deletion, FLT3 Amplification | MDM2 Deletion |  | 
| A-001 | A-010 | 3 | 2 | 1 | BRAF p.V600E, FLT3 Amplification | EWSR1--ZNRF3 | CDKN2A Deletion |
