# Median housing value prediction

The housing data can be downloaded from https://raw.githubusercontent.com/ageron/handson-ml/master/. The script has codes to download the data. We have modelled the median house value on given housing data.

The following techniques have been used:

 - Linear regression
 - Decision Tree
 - Random Forest

## Steps performed
 - We prepare and clean the data. We check and impute for missing values.
 - Features are generated and the variables are checked for correlation.
 - Multiple sampling techinuqies are evaluated. The data set is split into train and test.
 - All the above said modelling techniques are tried and evaluated. The final metric used to evaluate is mean squared error.

## Setup for development
### Create conda environment
```console
conda env create -f env.yml
conda activate <env_name>
```

### Perform test
Tox have been configured with pytest to automate testing in virtualenv.
```console
tox
```
Test a specific test file:
```console
tox -- -k <file_name>
```

## Usage
### Install package
#### Option 1. From github:
```console
git clone https://github.com/TejaML/mle-training.git
cd mle-training
pip install .
```
#### Option 2. From PyPi

```console
pip install housing-prediction
```

#### Test installation:
To test whether the package is successfully installed or not, start python session, and try to import housing. If it's imported successfully, then installation is complete

```console
python
>>> import housing
```


It will install all the dependencies and the housing package

### Run scripts

There are two ways to run the scripts, as single command line tool and as python scripts.

* As command line tool
    ```console
    housing
    ```

* As python scripts

```console
python -m housing.ingest_data
python -m housing.train
python -m housing.score
```

You can also access pass arguments, to find all available arguments:
```console
housing --help
python -m housing.ingest_data --help
python -m housing.train
python -m housing.score
```
