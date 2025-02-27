import pickle
from kipoi.data import Dataset
import pandas as pd
import numpy as np

def read_pickle(f):
    with open(f, "rb") as f:
        return pickle.load(f)

class MyDataset(Dataset):

    def __init__(self, features_file, targets_file=None, x_transformer=None, y_transformer=None):
        self.features_file = features_file
        self.targets_file = targets_file

        self.y_transformer = read_pickle(y_transformer)
        self.x_transformer = read_pickle(x_transformer)

        self.features = pd.read_csv(features_file)
        if targets_file is not None:
            self.targets = pd.read_csv(targets_file)
            assert len(self.targets) == len(self.features)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        x_features = np.ravel(self.x_transformer.transform(self.features.iloc[idx].values[np.newaxis]))
        if self.targets_file is None:
            y_class = {}
        else:
            y_class = np.ravel(self.y_transformer.transform(self.targets.iloc[idx].values[np.newaxis]))
        return {
            "inputs": {
                "features": x_features
            },
            "targets": y_class,
            "metadata": {
                "example_row_number": idx
            }
        }
