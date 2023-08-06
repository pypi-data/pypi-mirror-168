from pathlib import Path

import pandas as pd
import librosa
from librosa.core.spectrum import stft as _stft
from librosa.filters import mel, get_window
import numpy as np
from torch.utils.data import Dataset


def get_mel_basis(sr, n_fft, n_mels, fmin, fmax, htk=False, norm="slaney"):
    mel_basis = mel(sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=fmin, fmax=fmax, htk=htk, norm=norm)
    return mel_basis


def to_mel_scale(spec, mel_basis):
    """Compute mel-scale (magnitude, power) spectrum from linear (magnitude, power) spectrum."""
    mel_pspec = np.dot(spec, mel_basis)
    return mel_pspec


def to_lin_scale(mel_spec, mel_basis):
    """Compute linear (magnitude, power) spectrum from mel-scale (magnitude, power) spectrum."""
    bin_scaling = 1.0 / np.maximum(0.0005, np.sum(np.dot(mel_basis, mel_basis.T), axis=0))
    spec = bin_scaling[np.newaxis, :] * np.dot(mel_spec, mel_basis.T)
    return spec


def to_db(mspec):
    mspec = np.clip(mspec, 10 ** (-140.0 / 20), None)
    return 20 * np.log10(mspec)


class MelFBANK:
    def __init__(self, sr, hoptime, wintime, n_mels, fmin=10, fmax=4000):
        self.sr = sr
        self.hoptime = hoptime
        self.wintime = wintime
        self.n_mels = n_mels
        self.fmin = fmin
        self.fmax = fmax
        self.cond_hop = np.int32(hoptime * sr)
        self.fftsize = int(np.round(wintime * sr))
        self.ffthop = self.cond_hop
        self.nfftbin = self.fftsize // 2 + 1
        self.fftoverlap = self.fftsize // self.ffthop
        self.mel_basis = get_mel_basis(sr, self.fftsize, self.n_mels, fmin, fmax).astype(np.float32)

    def stft(self, audio):
        center = True
        window = 'hamming'
        fshift = int(np.round(self.hoptime * self.sr))

        win = get_window(window, self.fftsize, fftbins=True)
        k = 1. / (np.sum(win) / 2)  # scale

        spec = _stft(audio, n_fft=self.fftsize, hop_length=fshift, win_length=self.fftsize, window=window, center=center).T
        spec *= k
        return spec

    def __call__(self, audio):
        spec = self.stft(audio)
        mspec = np.abs(spec)  # magnitude spectrum
        mspec = to_mel_scale(mspec, self.mel_basis.T)
        mspec = to_db(mspec)
        return mspec


class ESCDataset(Dataset):
    def __init__(self, dataset_dir: str,
                 folds: list,
                 sr=8000,
                 hop_time=0.01,
                 win_time=0.025,
                 n_mel=128,
                 clamp_min_db=-140.0,
                 n_classes=50):
        self.data_dir = Path(dataset_dir)
        self.sr = sr
        self.logmelspec = MelFBANK(sr, hop_time, win_time, n_mel)
        self.folds = folds
        self.meta = self.get_meta()
        self.file_list = list(self.meta[self.meta['fold'].isin(folds)].filename)
        print(f"folds {folds} with total length {len(self.file_list)}")
        self.mean, self.std = self.load_stats()

    def get_meta(self):
        return pd.read_csv(self.data_dir / 'meta/esc50.csv')

    def get_stats(self):
        means = np.zeros(self.logmelspec.n_mels)
        std = np.zeros(self.logmelspec.n_mels)
        for recording in self.file_list:
            data = librosa.load(self.data_dir / ('audio/' + recording), sr=self.sr)[0]
            logmelspec = np.array(self.logmelspec(data), dtype=np.float)
            means += logmelspec.mean(axis=0)
        means /= len(self.file_list)
        for recording in self.file_list:
            data = librosa.load(self.data_dir / ('audio/' + recording), sr=self.sr)[0]
            logmelspec = np.array(self.logmelspec(data), dtype=np.float)
            std += (logmelspec.mean(axis=0) - means) ** 2
        std = np.sqrt(std / len(self.file_list))
        std[np.where(std == 0)] = 1.
        return means, std

    def load_stats(self):
        means = np.load("./data/esc_means.npy")
        std = np.load("./data/esc_std.npy")
        return means, std

    def normalize(self, logmelspec):
        return (logmelspec - self.mean) / self.std

    def __getitem__(self, index):
        recording = self.file_list[index]
        data = librosa.load(self.data_dir / ('audio/' + recording), sr=self.sr)[0]
        logmelspec = self.normalize(np.array(self.logmelspec(data), dtype=np.float))
        category = np.array(self.meta[self.meta.filename == recording].target.values[0], dtype=np.int64)

        return logmelspec, category

    def __len__(self):
        return len(self.file_list)
