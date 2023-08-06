# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_slizovskaia']

package_data = \
{'': ['*'], 'ast_slizovskaia': ['data/*']}

install_requires = \
['einops>=0.4.1,<0.5.0',
 'librosa>=0.9.2,<0.10.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pytorch-lightning>=1.3.8,<2.0.0',
 'torchaudio>=0.12.1,<0.13.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'ast-slizovskaia',
    'version': '0.1.4',
    'description': 'Test exercise AST model on the ESC-50 dataset',
    'long_description': '# Test implementation for Audio Spectrogram Transformer by Olga Slizovskaia\n\nThis repository provides a test implementation of the Audio Spectrogram Transformer described in the original [paper](https://arxiv.org/pdf/2104.01778.pdf).\nPlease, note, that this implementation is lacking several important details compared to the original paper, such as dataset normalization, data augmentation routines and optimal hyperparameters selection. \nThe results that you will obtain using the code provided in this repository, will differ severely from the results reported in the original paper. \n\n## Requirements\n\nThis repository requires a working python3.9 installation and uses poetry for dependency management and packaging.  \nPlease, install [poetry](https://python-poetry.org/docs/#installation) using the official guidelines.\n\nYou also need to download the [ESC-50 dataset](https://dagshub.com/kinkusuma/esc50-dataset) and \nspecify the path to the dataset as ```dataset_dir``` parameter in [hparams.py](./ast_slizovskaia/hparams.py) configuration file.\n\n## Installation\n\nTo install all necessary dependencies, run:\n\n```poetry env use 3.9```\n\n```poetry install```\n\n## Usage\n\nWe use the standard 5-fold cross-validation scheme for evaluating the classification model. The folds are defined in the datasets meta file and hardcoded for training.\nTo train and evaluate the model, run:\n\n```python train.py```\n\nor\n\n```poetry run python train.py ```.\n\n## Results\n\nThe best test accuracy score achieved with this model without any pretraining is 0.39 as you can see in the following plot:\n\n![test_accuracy](./ast_slizovskaia/data/test_accuracy.png)\n\nThe model overfits singnificantly reaching training loss values as low as 1.8 and only reaching validation and test loss values about 2.3.\n',
    'author': 'Olga Slizovskaia',
    'author_email': 'oslizovskaia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
