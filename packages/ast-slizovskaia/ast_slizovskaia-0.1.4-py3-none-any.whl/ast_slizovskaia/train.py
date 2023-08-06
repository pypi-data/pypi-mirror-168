import importlib
from argparse import ArgumentParser, Namespace
from typing import Union, List, Dict

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.strategies import DDPStrategy

from dataset import ESCDataset
from model import ASTModel


class ASTDataModule(pl.LightningDataModule):
    """PyTorch Lightning DataModule that defines training and validation datasets for AST training
    with the melspec dataset"""
    def __init__(self, params, fold_id: int = 1):
        super().__init__()

        folds = [[[2, 3, 4], [5], [1]],
                 [[3, 4, 5], [1], [2]],
                 [[1, 4, 5], [2], [3]],
                 [[1, 2, 5], [3], [4]],
                 [[1, 2, 3], [4], [5]]]

        self.batch_size = params.batch_size
        self.num_workers = params.n_workers
        self.pin_memory = params.light_loader
        self.train_data = ESCDataset(dataset_dir=params.dataset_dir,
                                     folds=folds[fold_id][0],
                                     sr=params.sr,
                                     hop_time=params.hop_time,
                                     win_time=params.win_time,
                                     n_mel=params.n_mel)
        self.val_data = ESCDataset(dataset_dir=params.dataset_dir,
                                   folds=folds[fold_id][1],
                                   sr=params.sr,
                                   hop_time=params.hop_time,
                                   win_time=params.win_time,
                                   n_mel=params.n_mel)
        self.test_data = ESCDataset(dataset_dir=params.dataset_dir,
                                    folds=folds[fold_id][2],
                                    sr=params.sr,
                                    hop_time=params.hop_time,
                                    win_time=params.win_time,
                                    n_mel=params.n_mel)

    def train_dataloader(
        self,
    ) -> Union[DataLoader, List[DataLoader], Dict[str, DataLoader]]:
        """Create train dataloader with a predefined train dataset """
        return DataLoader(
            self.train_data,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=True,
        )

    def val_dataloader(self) -> Union[DataLoader, List[DataLoader]]:
        """Create train dataloader with a predefined validation dataset """
        return DataLoader(
            self.val_data,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=False,
        )

    def test_dataloader(self) -> Union[DataLoader, List[DataLoader]]:
        return DataLoader(
            self.test_data,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
            shuffle=False,
        )


def train(hparams):
    """Creates DataModule, defines the model and callbacks.
    Defines the trainer and runs a tuner from pytorch lightning if auto_lr_find is specified.
    Trains the model and saves the final swa checkpoint in numpy format."""

    for fold_id in range(5):
        checkpoint_callback = ModelCheckpoint(
            monitor="val_loss",
            filename="ast-{epoch:03d}-{val_los:.4f}",
            save_last=True,
        )
        trainer = pl.Trainer(
            accelerator="gpu",
            devices=hparams.gpus,
            strategy=DDPStrategy(find_unused_parameters=False),
            max_epochs=hparams.n_epochs,
            fast_dev_run=hparams.fast_dev_run,
            auto_lr_find=hparams.auto_lr_find,
            auto_scale_batch_size=hparams.auto_scale_batch_size,
            log_every_n_steps=hparams.summary_step,
            callbacks=[checkpoint_callback],
        )
        data_module = ASTDataModule(hparams, fold_id)
        model = ASTModel(hparams)
        if hparams.auto_lr_find:
            trainer.tune(model, datamodule=data_module)
        trainer.fit(model, datamodule=data_module)
        trainer.test(ckpt_path="best", datamodule=data_module)


def main():
    """Seed all modules, parse arguments and run training"""
    pl.seed_everything(1234, workers=True)

    parser = ArgumentParser()
    parser.add_argument("--exp_config", default="hparams", type=str)
    args = parser.parse_args()
    hparams = importlib.import_module(args.exp_config)
    params = dict([(elem, hparams.__dict__[elem]) for elem in hparams.__dict__ if not elem.startswith("_")])
    train(Namespace(**params))


if __name__ == "__main__":
    main()
