# Formatted inputs
Input data must be formatted for annotation by the Molecular Oncology Almanac for use with matchmaking. Five inputs are required to run,
- samples to consider
- somatic variants
- called copy number alterations
- fusions
- samples labeled by therapy response (or the label used for matchmaking)

Samples also must be compared in a pairwise fashion to annotate for which samples share a label. This can be done with the `pairwise-comparison.py` script in this directory. File are passed to each script individually, so there is not an enforced naming convention. 

## Samples
A tab-delimited text file containing all samples to consider must be prepared. Samples should be labeled with the column `sample_name` and the file can contain as many other annotations or columns as you would like for your own organization, they will not be used by the code in this repository.

### Required fields
The following column names are required for the samples input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient

### Example
| sample_name | tumor_type | age |
| -- | -- | -- |
| A-001 | ovarian | 60 |
| A-002 | nsclc | 42 |

### Somatic variants
A tab-delimited text file containing all somatic variants to consider must be prepared, containing the sample name, gene, variant classification, and protein change. 

### Required fields
The following column names are required for the somatic variants input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient as contained in the samples input file
- `feature`, gene symbol associated with the variant
- `alteration_type`, variant consequence or classification resulting from the nucleotide change
- `alteration`, protein change associated with the variant using the one-letter amino-acid codes

Accepted values for `alteration_type` include `Missense`, `Nonsense`, `Nonstop`, `Frameshift`, `Splice Site`, `Deletion`, and `Insertion`. 

| feature | alteration_type | alteration | sample_name |
| -- | -- | -- | -- | -- |
| ERCC2 | Missense | p.R647C | A-001 |
| TP53 | Nonsense | p.E258*	| A-001 |
| EGFR | Frameshift | p.E543fs | A-002 |
| CDK1 | Splice Site | | A-002 | A-003 |
| BRAF | Deletion | p.GAGA30del	| A-003 |
| EZH2 | Insertion | p.185_185D>DD | A-004 |
| PTEN | Nonstop | p.*404L | A-005 |

### Called copy number alterations

### Fusions

### Samples labeled by therapy response

### Pairwise comparison of labeled samples
