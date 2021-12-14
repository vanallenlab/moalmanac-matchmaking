# Matchmaking from Molecular Oncology Almanac
Template repository to perform profile-to-cell line matchmaking

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

### Setting font to arial


## Citation
Please cite our paper if using any information or code from this repository  
> [Reardon, B., Moore, N.D., Moore, N.S., *et al*. Integrating molecular profiles into clinical frameworks through the Molecular Oncology Almanac to prospectively guide precision oncology. *Nat Cancer* (2021). https://doi.org/10.1038/s43018-021-00243-3](https://www.nature.com/articles/s43018-021-00243-3)

