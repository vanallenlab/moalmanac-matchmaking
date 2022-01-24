# Formatted inputs
Input data must be formatted for annotation by the Molecular Oncology Almanac for use with matchmaking. Five inputs are required to run,
- [samples to consider](#samples)
- [somatic variants](#somatic-variants)
- [called copy number alterations](#called-copy-number-alterations)
- [fusions](#fusions)
- [samples labeled by therapy response (or the label used for matchmaking)](#labeled-samples)

File are passed to each script individually, so there is not an enforced naming convention. 

Formatted example data, as used in the present study, are also found in this directory,
- samples to consider: `samples.summary.txt`
- somatic variants: `samples.somatic_variants.txt`
- called copy number alterations: `samples.copy_numbers.txt`
- fusions: `samples.fusions.txt`
- labeled samples: `samples.sensitive_therapies.txt`

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

[Return to top](#formatted-inputs)

## Somatic variants
A tab-delimited text file containing all somatic variants to consider must be prepared, containing the sample name, gene, variant classification, and protein change. 

### Required fields
The following column names are required for the somatic variants input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient as contained in the samples input file
- `feature`, gene symbol associated with the variant
- `alteration_type`, variant consequence or classification resulting from the nucleotide change
- `alteration`, protein change associated with the variant using the one-letter amino-acid codes

Accepted values for `alteration_type` include `Missense`, `Nonsense`, `Nonstop`, `Frameshift`, `Splice Site`, `Deletion`, and `Insertion`. 

### Example
| feature | alteration_type | alteration | sample_name |
| -- | -- | -- | -- | 
| ERCC2 | Missense | p.R647C | A-001 |
| TP53 | Nonsense | p.E258*	| A-001 |
| EGFR | Frameshift | p.E543fs | A-002 |
| CDK1 | Splice Site | | A-002 | A-003 |
| BRAF | Deletion | p.GAGA30del	| A-003 |
| EZH2 | Insertion | p.185_185D>DD | A-004 |
| PTEN | Nonstop | p.*404L | A-005 |

[Return to top](#formatted-inputs)

## Called copy number alterations
A tab-delimited text file containing all called copy number alterations to consider must be prepared, containing the sample name, gene, and called event. 

### Required fields
The following column names are required for the called copy number alterations input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient as contained in the samples input file
- `feature`, gene symbol associated with the copy number event
- `alteration_type`, direction of copy number event

Accepted values for `alteration_type` include `Amplification` and `Deletion`

### Example
| feature | alteration_type | sample_name |
| -- | -- | -- | 
| TP53 | Deletion | A-001 |
| EGFR | Amplification | A-002 |
| CDKN2A | Amplification | A-002 |

[Return to top](#formatted-inputs)

## Fusions
A tab-delimited text file containing all fusions to consider must be prepared, containing the sample name, primary gene involved, and partner gene. 

### Required fields
The following column names are required for the fusions input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient as contained in the samples input file
- `feature`, gene symbol associated with the fusion's primary gene
- `partner`, gene symbol associated with the fusion's partner gene

### Example
| feature | partner | sample_name |
| -- | -- | -- | 
| BCR | ABL1 |	A-001 |
| COL1A1 | PDGFB | A-002 |
| TMPRSS2 | ERG | A-002 |

[Return to top](#formatted-inputs)

## Labeled samples
A tab-delimited text file containing all labels per sample must be prepared, containing one sample-label pair per row. Multiple rows per sample can exist; for example, if a sample is treated with multiple therapies. 

### Required fields
The following column names are required for the labeled samples input file. Column names are case-sensitive.
- `sample_name`, string associated with each sample, molecular profile, or patient as contained in the samples input file
- `{label name}`, the string associated with the label used. This column must exist but does not enforce a specific column name, the string will be passed to relevant scripts.

### Example
| sample_name | therapy_name |
| -- | -- | 
| A-001 | Dabrafenib |	A-001 |
| A-001 | Vemurafenib | A-001 |
| A-002 | Imatinib | A-002 |

[Return to top](#formatted-inputs)
