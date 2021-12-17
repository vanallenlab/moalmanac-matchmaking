# Matchmaking from Molecular Oncology Almanac
Template repository to perform profile-to-profile matchmaking. 

Matchmaking is a framework to identify genomically similar molecular profiles and evaluate that similarity profile based on shared labels, such as drug sensitivity. This repository contains data for cancer cell lines as represented in the [present study](https://www.nature.com/articles/s43018-021-00243-3), and can be revised to perform matchmaking on other cohorts.

Documentation detailing how to use code within this repository can be found in the [`matchmaking/`](matchmaking) folder.

## Installation
### Download
This repository can be downloaded through GitHub by either using the website or terminal. To download on the website, navigate to the top of this page, click the green `Clone or download` button, and select `Download ZIP` to download this repository in a compressed format. To install using GitHub on terminal, type 

```bash
git clone https://github.com/vanallenlab/moalmanac-matchmaking.git
cd moalmanac-matchmaking
```

### Python dependencies
This repository uses Python 3.9. We recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and running Python with either [Anaconda](https://www.anaconda.com/download/) or  [Miniconda](https://conda.io/miniconda.html). 

Run the following from this repository's directory to create a virtual environment and install dependencies with Anaconda or Miniconda,
```bash
conda create -y -n matchmaking python=3.9
conda activate matchmaking
pip install -r requirements.txt
```

Or, if using base Python, 
```bash
virtualenv venv
source activate venv/bin/activate
pip install -r requirements.txt
```

To make the virtual environment available to jupyter notebooks, execute the following code while the virtual environment is activated,
```bash
ipython kernel install --user --name=matchmaking
```

## Updates to this template
If updates are made to this repository after you have begun using the template, you can fetch updates from this repository by using the following code from your repository,
```bash
git remote add template https://github.com/vanallenlab/moalmanac-matchmaking.git
git fetch --all
git merge template/main
```

## Citation
Please cite our paper if using any information or code from this repository  
> [Reardon, B., Moore, N.D., Moore, N.S., *et al*. Integrating molecular profiles into clinical frameworks through the Molecular Oncology Almanac to prospectively guide precision oncology. *Nat Cancer* (2021). https://doi.org/10.1038/s43018-021-00243-3](https://www.nature.com/articles/s43018-021-00243-3)

A protocol has also been published to accompany the above study, detailing how matchmaking is performed,
> [Reardon, B. & Van Allen, E. M. Molecular profile to cancer cell line matchmaking. Protocol Exchange https://doi.org/10.21203/rs.3.pex-1539/v1 (2021).](https://protocolexchange.researchsquare.com/article/pex-1539/v1)
