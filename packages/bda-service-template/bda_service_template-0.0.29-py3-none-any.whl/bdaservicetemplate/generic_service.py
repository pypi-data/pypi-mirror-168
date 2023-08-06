from bdaserviceutils import get_args


class GenericService():
    def __init__(self, parser):
        super().__init__()
        
        # Raw args
        self._args = get_args()
        
        self.parser = parser
        # Parsed args
        self.args = self.parser.parse_args()


    def get_datasets(self):
        datasets = {}
        for dataset in self.parser.input_datasets:
            datasets[dataset.name] = self.get_dataset(dataset.name)

        # If only one dataset, return it directly
        if len(datasets) == 1:
            return datasets[next(iter(datasets))]

        return datasets

    def save_datasets(self, datasets):
        if isinstance(datasets, dict):
            for dataset in self.parser.output_datasets:
                self.save_dataset(datasets[dataset.name], dataset.name)
        # If only one dataset a dictionary is not expected
        else:
            self.save_dataset(datasets, self.parser.output_datasets[0].name)


    def download_models(self):
        models = {}
        for model in self.parser.input_models:
            models[model.name] = self.download_model(model.name)
        
        # If only one model, return it directly
        if len(models) == 1:
            return models[next(iter(models))]
        
        return models

    def upload_models(self, models):     
        if isinstance(models, dict):
            for model in self.parser.output_models:
                self.upload_model(models[model.name], model.name)   
        # If only one dataset a dictionary is not expected
        else:
            self.upload_model(models, self.parser.output_models[0].name)
