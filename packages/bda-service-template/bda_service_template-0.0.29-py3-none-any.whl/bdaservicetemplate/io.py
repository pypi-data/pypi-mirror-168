import os

class IO:
    @staticmethod
    def dataset_to_dataset(func):
        
        def wrapper(*args):
            self = args[0]
            datasets = self.get_datasets()
            resulting_dataset = func(self, datasets)
            self.save_dataset(resulting_dataset)

        return wrapper


    @staticmethod
    def dataset_to_model(func):
        
        def wrapper(*args):
            self = args[0]
            datasets = self.get_datasets()
            model_path = func(self, datasets)
            self.upload_model(model_path)

        return wrapper


    @staticmethod
    def dataset_and_model_to_dataset(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            model_path = self.download_model()
            resulting_dataset = func(self, dataset, model_path)
            self.save_dataset(resulting_dataset)

        return wrapper

    @staticmethod
    def dataset_to_dataset_and_model(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            resulting_dataset, resulting_model = func(self, dataset)
            self.save_dataset(resulting_dataset)
            self.upload_model(resulting_model)

        return wrapper

    @staticmethod
    def dataset_and_model_to_dataset_and_model(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            model_path = self.download_model()
            resulting_dataset, resulting_model = func(self, dataset, model_path)
            self.save_dataset(resulting_dataset)
            self.upload_model(resulting_model)

        return wrapper

    @staticmethod
    def io(func):
        def wrapper(*args):
            self = args[0]
            
            args_to_pass = {}

            if len(self.parser.input_datasets) > 0:
                datasets = self.get_datasets()
                args_to_pass['datasets' if len(self.parser.input_datasets) > 1 else 'dataset'] = datasets
            
            if len(self.parser.input_models) > 0:
                models = self.download_models()
                args_to_pass['models' if len(self.parser.input_models) > 1 else 'model'] = models

            result = func(self, **args_to_pass)

            if len(self.parser.output_datasets) > 0:
                if isinstance(result, tuple):
                    datasets = result[0]
                else:
                    datasets = result
                self.save_datasets(datasets)
            
            if len(self.parser.output_models) > 0:
                if isinstance(result, tuple):
                    models = result[1]
                else:
                    models = result            
                self.upload_models(models)

        return wrapper

