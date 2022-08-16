# Matchmaking
Matchmaking identifies genomic similarity between provided molecular profiles within a cohort and evaluates genomic similarity based on shared labels. This repository contains an implementation of matchmaking as demonstrated in the [present study](https://www.nature.com/articles/s43018-021-00243-3), which perform a hold-one-out approach to compare cancer cell lines based on genomic similarity with the goal of finding nearest neighbors that share therapeutic sensitivity. 

To adapt your own data for matchmaking, follow instructions under [`inputs/`](inputs) to format and annotate molecular data, sample information, and labels for your cohort. Datasources as used in the present study are found in the [`inputs/datasources/`](inputs/datasources) folder.

Documentation detailing outputs can be found in the [`outputs/`](outputs) folder. All outputs committed to GitHub were generated using a subset of cell lines used in the present study (n=50) to ensure that output files are less than the GitHub file size limit.

## Calculate genomic distances from models
The script `calculate-distances.py` is used to calculate the genomic similarity of a provided cohort using all models that were evaluated for the present study. Annotated data is further processed for individual models, as implemented in [`models.py`](models.py) and called in the main function of [`calculate-distances.py`](calculate-distances.py). A description for each model is provided in the [`models.py`](models.py) file and additional information can be found in the [protocol](https://protocolexchange.researchsquare.com/article/pex-1539). 

To run this script, edit or copy and edit the `handle` fields of all keys within `config.default.json` to suit your data.

### Usage
Required arguments:
```bash
    --config, -c    <string>  File handle to annotated somatic variants                
```

Example:
```bash
python calculate-distances.py --config config.default.json 
```

## Evaluate genomic similarity models
The script `evaluate-models.py` will compare the results of genomic distance and/or similarity models applied to a provided cohort, generated from [calculate-distances.py](#calculate-genomic-distances-from-models). Genomic comparisons between two samples are evaluated as relevant or not relevant based on if they share a provided label. For more details, see the slides on [evaluation metrics](../docs/matchmaking-evaluation-metrics.pdf) or the [protocol](https://protocolexchange.researchsquare.com/article/pex-1539). 

To run this script, 

### Usage
Required arguments:
```bash
    --labels, -l    <string>  A tab delimited file containing pairwise comparison of sample labels of interest
    --samples, -s   <string>  A tab delimited file containing which samples to use, listed in a column with a column name sample_name
```

Optional arguments:
```bash
    --distance, -d            <string>  A tab delimited file containing a column for the case sample name, comparison sample name, and at least one column containing distance values (0 = more similar) for sample comparisons
    --affinity, -a            <string>  A tab delimited file containing a column for the case sample name, comparison sample name, and at least one column containing similarity values (1 = more similiar) for sample comparisons
    --features, -f            <string>  A tab delimited file containing pairwise comparison of features
    --output_directory, -o    <string>  Name of output directory to create, if it does not already exist, and place output files
```

Example:
```bash
python evaluate_models.py \
  -l inputs/pairwise-comparisons/samples.pairwise-labels.txt \
  -s inputs/formatted/samples.summary.txt \
  -d outputs/distances/jaccard-almanac-genes.stacked.txt \
  -d outputs/distances/jaccard-cgc-genes.stacked.txt \
  -f inputs/pairwise-comparisons/samples.pairwise-features.txt \
  -o outputs
```

Here, we compare two distance models generated: jaccard-almanac-genes and jaccard-cgc-genes. Currently, these two models are defined in [models.py](models.py) within the `AlmanacGenes` and `CGC` classes. Rather than pass two distance files, we could horizontally concatenate the two files together and pass a single file with this argument. Models passed with the `--affinity` argument will have their similarity values changed to distances by subtracting the observed value from 1.  

## Compare models
The script `compare-models.py` is used to perform two tasks from the `.pkl` produced by `evaluate-models.py`,
1. Create a summary table of model performance, [`outputs/models.summary.txt`](outputs/models.summary.txt)
2. Perform pairwise comparison of models to see if models significantly differ from one another, [`outputs/models.pairwise-comparison.txt`](outputs/models.pairwise-comparison.txt)

The second task of this script can take up to tens of minutes to run. 

### Usage
Required arguments:
```bash
   --input, -i              <string> File handle to .pkl output from `evaluate-models.py`
   --output_directory, -o   <string> Output path to write produced files to
```

Example:
```bash
python compare-models.py --input outputs/models.evaluated.pkl --output_directory outputs/
```

## Modifying code in this repository
Models can be revised or added by editing the [`models.py`](models.py) file and evaluation metrics can be revised by modifying the [`metrics.py`](metrics.py) file. Figures generated can be modified by revising the [`plots.py`](plots.py) file.

## References
1. [Reardon, B. & Van Allen, E. M. Molecular profile to cancer cell line matchmaking. Protocol Exchange https://doi.org/10.21203/rs.3.pex-1539/v1 (2021).](https://protocolexchange.researchsquare.com/article/pex-1539/v1?redirect=/article/pex-1539)
2. [Reardon, B., Moore, N.D., Moore, N.S., et al. Integrating molecular profiles into clinical frameworks through the Molecular Oncology Almanac to prospectively guide precision oncology. Nat Cancer (2021). https://doi.org/10.1038/s43018-021-00243-3](https://doi.org/10.1038/s43018-021-00243-3)
3. [Ghandi, M. et al. Next-generation characterization of the Cancer Cell Line Encyclopedia. Nature 569, 503–508 (2019).](https://www.nature.com/articles/s41586-019-1186-3)
4. [Yang, W. et al. Genomics of Drug Sensitivity in Cancer (GDSC): a resource for therapeutic biomarker discovery in cancer cells. Nucleic Acids Res. 41, D955–61 (2013).](https://academic.oup.com/nar/article/41/D1/D955/1059448)
5. [Sondka, Z. et al. The COSMIC Cancer Gene Census: describing genetic dysfunction across all human cancers. Nat. Rev. Cancer 18, 696–705 (2018).](https://www.nature.com/articles/s41568-018-0060-1)
6. [Wang, B. et al. Similarity network fusion for aggregating data types on a genomic scale. Nat. Methods 11, 333–337 (2014).](https://www.nature.com/articles/nmeth.2810)
7. [Stanford CS276, Introduction to Information Retrieval by Chris Manning and Pandu Nayak](https://web.stanford.edu/class/cs276/handouts/EvaluationNew-handout-1-per.pdf)
8. [Purdue, Significance Testing Tutorial by Avi Kak](https://engineering.purdue.edu/kak/SignificanceTesting.pdf)
