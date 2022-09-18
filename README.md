# FDS logs analysis

This repository contains mush.vg logs from the FDS for datamining purposes.
It contains example notebooks to make you started.

## Getting started
You need **Python 3.10+** to use the notebooks of this repository.

- Clone the project : `git clone git@gitlab.com:eternaltwin/mush/fds-logs-analysis.git`
- Create a virtual environnement with your preferred solution and install the packages from `requirements.txt`.
(If you use Miniconda/Anaconda : `conda create -n fds_logs_analysis python=3.10` > `conda activate fds_logs_analysis` > `pip install -r requirements.txt`)

And then you're done!

## Repo Architecture

```
|-- data/ --> FDS logs in ZIP format
|-- notebooks/ --> thematic data analysis notebooks 
|-- scripts/  --> scripts to preprocess raw data
```