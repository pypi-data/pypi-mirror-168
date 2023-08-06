from .generic_service import GenericService
import pandas as pd
import os
from fileioutilities.file_io import FileIO
from dsioutilities import Dataset
from alidaargparser import get_asset_property

class PandasService(GenericService):
    def __init__(self, parser):
        super().__init__(parser)

    def get_dataset(self, name="input-dataset"):
        input_dataset = Dataset(name, dataset_type="tabular")
        
        # If list of csv concatenate them
        if isinstance(input_dataset.get_path(), list):
            df = pd.concat([pd.read_csv(filename) for filename in input_dataset.get_path()])
        else:
            df = pd.read_csv(input_dataset.get_path())
        
        # TODO select by type
        # Select specified columns
        input_cols = get_asset_property(name, "input_columns")
        if input_cols is not None and input_cols != "ANY" and input_cols != "NUMBER":
            df = df[input_cols.split(",")]
        return df

    def save_dataset(self, dataset: pd.DataFrame, name="output-dataset"):
        dataset.to_csv(Dataset(name, dataset_type="tabular").get_path(), index=False)

    def download_model(self, name='input_model'):
        path = os.path.join(".", "model")
        FileIO(name=name).download(local_path=path)
        return path

    def upload_model(self, path, name='output_model'):
        fileIO = FileIO(name=name)
        fileIO.upload(local_path=path)
