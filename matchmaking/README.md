# Matchmaking
Matchmaking identifies genomic similarity between provided molecular profiles within a cohort and evaluates genomic similarity based on shared labels. This repository contains an implementation of matchmaking as demonstrated in the [present study](https://www.nature.com/articles/s43018-021-00243-3), which perform a hold-one-out approach to compare cancer cell lines based on genomic similarity with the goal of finding nearest neighbors that share therapeutic sensitivity. 

To adapt your own data for matchmaking, follow instructions under [`inputs/`](inputs) to format and annotate molecular data, sample information, and labels for your cohort. Datasources as used in the present study are found in the [`inputs/datasources/`](inputs/datasources) folder.

The script `evaluate-models.py` is used to evaluate matchmaking models on a provided cohort. Annotated data is further processed for individual models, as implemented in [`models.py`](models.py) and called in the main function of [`evaluate-models.py`](evaluate-models.py). A description for each model is provided in the [`models.py`](models.py) file and additional information can be found in the [protocol](https://protocolexchange.researchsquare.com/article/pex-1539).

Documentation detailing outputs can be found in the [`outputs/`](outputs) folder.

## Usage
Required arguments:
```bash
    --variants, -v                    <string>  File handle to annotated somatic variants
    --copy_number_alterations, -cn    <string>  File handle to annotated copy number copy_number_alterations
    --fusions, -f                     <string>  File handle to annotated fusions
    --fusions_gene1, -f1              <string>  File handle to annotated fusions, focusing on gene1
    --fusions_gene2, -f2              <string>  File handle to annotated fusions, focusing on gene2
    --samples, -s                     <string>  File handle to sample information and which samples to use
    --labels, -l                      <string>  File handle to sample labels
    --pairwise, -p                    <string>  File handle to pairwise comparisons of sample labels
    --moalmanac, -m                   <string>  File handle to molecular oncology almanac json
    --cgc, -c                         <string>  File handle to cancer gene census                   
```

Example:
```bash
python evaluate-models.py --samples inputs/formatted/summary.txt \
                          --labels inputs/formatted/samples.sensitive_therapies.txt \
                          --pairwise inputs/formatted/samples.pairwise.txt \
                          --variants inputs/annotated/samples.variants.annotated.txt \
                          --copy_number_alterations inputs/annotated/samples.copy_numbers.annotated.txt \
                          --fusions inputs/annotated/samples.fusions.annotated.txt \
                          --fusions_gene1 inputs/annotated/samples.fusions.annotated.gene1.txt \
                          --fusions_gene2 inputs/annotated/samples.fusions.annotated.gene2.txt 
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
