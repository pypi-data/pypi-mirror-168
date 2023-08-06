# Test implementation for Audio Spectrogram Transformer by Olga Slizovskaia

This repository provides a test implementation of the Audio Spectrogram Transformer described in the original [paper](https://arxiv.org/pdf/2104.01778.pdf).
Please, note, that this implementation is lacking several important details compared to the original paper, such as dataset normalization, data augmentation routines and optimal hyperparameters selection. 
The results that you will obtain using the code provided in this repository, will differ severely from the results reported in the original paper. 

## Requirements

This repository requires a working python3.9 installation and uses poetry for dependency management and packaging.  
Please, install [poetry](https://python-poetry.org/docs/#installation) using the official guidelines.

You also need to download the [ESC-50 dataset](https://dagshub.com/kinkusuma/esc50-dataset) and 
specify the path to the dataset as ```dataset_dir``` parameter in [hparams.py](./ast_slizovskaia/hparams.py) configuration file.

## Installation

To install all necessary dependencies, run:

```poetry env use 3.9```

```poetry install```

## Usage

We use the standard 5-fold cross-validation scheme for evaluating the classification model. The folds are defined in the datasets meta file and hardcoded for training.
To train and evaluate the model, run:

```python train.py```

or

```poetry run python train.py ```.

## Results

The best test accuracy score achieved with this model without any pretraining is 0.39 as you can see in the following plot:

![test_accuracy](./ast_slizovskaia/data/test_accuracy.png)

The model overfits singnificantly reaching training loss values as low as 1.8 and only reaching validation and test loss values about 2.3.
