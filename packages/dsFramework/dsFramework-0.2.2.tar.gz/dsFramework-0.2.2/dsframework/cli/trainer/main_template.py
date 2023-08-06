import os
from os.path import exists
from pathlib import Path
import csv
import shutil
from pytorch_lightning.loggers import LightningLoggerBase, TensorBoardLogger
from comparison import generatedProjectNameComparison
from config import config
from data import generatedProjectNameData
from model import generatedProjectNameModel
from test import generatedProjectNameTest
from train import generatedProjectNameTrain
from tester.general_tester import generatedProjectNameGeneralTester
from dataset_preparation import generatedProjectNameDatasetPreparation

##
# @file
# @brief Main class.


class Main:
    """! Trainer main class, this is where all training components orchestrate.

    Its main job is to run:
    - training - train the model using train dataset and validation dataset.
    - testing - running model against test dataset.
    - eval - running the same test dataset

    Important node:
    It includes a split() method, which needs to be implemented. This is where the dataset gets split to
    train, validation and test datasets.

    """
    model_config = None
    trainer_config = None

    def __init__(self,
                 cfg=None,
                 training_path=None,
                 validation_path=None,
                 test_dataset_path=None,
                 force_dataset_split=False):

        self.training_path = training_path
        self.validation_path = validation_path
        self.test_dataset_path = test_dataset_path
        self.force_dataset_split = force_dataset_split

        """! Trainer main initializer."""
        self.save_path = None
        self.train_class = None
        self.model_class = None
        self.data_class = None
        self.data_class_test = None
        self.test_class = None
        self.model_config = cfg['model_config']
        self.trainer_config = cfg['trainer_config']
        self.metrics_config = cfg['metrics']
        self.dataset_config = cfg['dataset_config']
        self.dataset = None
        self.dataset_train = None
        self.dataset_validation = None
        self.dataset_test = None
        self.eval_res = None

        if (not training_path or not validation_path) and not test_dataset_path:
            raise 'Please provide paths for training and validation or test datasets in Main.'

        if not (self.test_dataset_path and exists(self.test_dataset_path)):
            if self.force_dataset_split or not self.training_path or not exists(self.training_path):
                self.prepare_datasets()

    def prepare_datasets(self):
        """! Implement this method to prepare/split the dataset to train/val/test datasets:
        For the trainer supply: dataset_train, self.dataset_validation
        For test supply: self.dataset_test

        Example:
            self.dataset = datasets.MNIST(self.dataset_path, download=True, train=True,
                                      transform=transforms.ToTensor())
            self.dataset_train, self.dataset_validation = random_split(self.dataset, [55000, 5000])
            self.dataset_test = datasets.MNIST(self.dataset_path, download=True, train=False,
                                           transform=transforms.ToTensor())

        Another example:
            dataset_prep = generatedProjectNameDatasetPreparation()

            train_dataset_path,
            val_dataset_path,
            test_dataset_path = dataset_prep.prepare_datasets(self.dataset_path, save_datasets=self.save_split_datasets,
                save_path=self.dataset_path, config=self.dataset_config)

        """

        #  raise 'Dataset Main.prepare_datasets() not implemented exception.'
        pass

    def save_dataset(self, dataset_path):
        """! Saves a copy of the dataset in /training_output/v1 folder zipped.

        In a later stage the trained model is created in the same folder, so we have a pair of the model and the
        dataset used to create it.
        """
        if not self.dataset_config['save_dataset']:
            return

        if os.path.isdir(dataset_path):
            if os.listdir(dataset_path):
                shutil.make_archive(os.path.join(self.save_path, 'dataset'), 'zip', dataset_path)

    def execute_trainer(self):
        """ Executes training process. it initializes the main 3 trainer modules:

        generatedProjectNameData - Class for holding datasets and functionality related to dataset handling
        generatedProjectNameModel - Network definition and all functionality related to creating the model.
        generatedProjectNameTrain - Execute trainer and all trainer related functionality.
        """

        self.save_path = self._save_path()

        self.model_class = generatedProjectNameModel(
            model_config=self.model_config,
            metrics_config=self.metrics_config,
            trainer_config=self.trainer_config,
            save_path=self.save_path)

        self.data_class = generatedProjectNameData(
            model_config=self.model_config,
            load_datasets=True,
            training_path=self.training_path,
            validation_path=self.validation_path,
            tokenizer=self.model_class.model.tokenizer)

        self.train_class = generatedProjectNameTrain(
            trainer_config=self.trainer_config,
            model_config=self.model_config,
            data_module=self.data_class.get_data_module(),
            model=self.model_class.get_model(),
            save_path=self.save_path)

        self.train_class.execute()

        self.save_dataset(self.training_path)

    def execute_test(self, model_path):
        """ Executes test process. runs the model against a test dataset.

        Initializes:
            generatedProjectNameData - Created with test dataset.
            generatedProjectNameTest - Loads model and executes test.

        Args:
            model_path: Path to saved model
        Returns:
            mmodel_test_results: Metrics - defined in config.
        """

        self.save_path = self._save_path()

        self.test_class = generatedProjectNameTest(
            model_path=model_path,
            test_dataset_path=self.test_dataset_path,
            trainer_config=self.trainer_config,
            model_config=self.model_config,
            metrics_config=self.metrics_config,
            save_path=self.save_path
        )

        model_test_results = self.test_class.execute_test()

        return model_test_results

    def execute_eval(self):
        """ Executes evaluation process on an existing model against a test dataset.

        Notes:
            Test dataset must be in Pandas dataframe format.

        Returns:
            eval_res - Evaluation metrics result.

        Result format example:
            self.eval_res = {'precision': 1.1, 'accuracy': 1.2, 'recall': 1.3, 'f1': 1.4,
                            'confusion_matrix': {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}}
        """

        model_tester = generatedProjectNameGeneralTester()

        try:
            output_path = model_tester.test_from_dataset(self.dataset_test, 1)
            self.eval_res = self.get_eval_results(output_path)

        except Exception as e:
            print(f'Could not start evaluation process: {e}')

        return self.eval_res

    def get_eval_results(self, output_path):
        """Reads evaluation results from path and returns it.

        Args:
            output_path - Location of eval results

        Returns:
            evaluation results - In dictionary format.

        """
        if exists(output_path):
            return csv.DictReader(open(output_path))
        else:
            return None

    def _save_path(self):
        """Returns the save path, based on the next version number."""
        if isinstance(self.trainer_config['logger'], TensorBoardLogger):
            output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'training_output')
            version_num = self._get_next_folder_num(output_path)
            self.trainer_config['logger'] = TensorBoardLogger(save_dir=os.getcwd(), version=f'v{version_num}',
                                                              name='training_output')
            save_path = self._get_save_path(create=False)
        else:
            save_path = self._get_save_path(create=True)

        return save_path

    def _get_save_path(self, create=False):
        """Create the next version folder (v1, v2, v3 ... vn) inside training_output folder.

        Returns:
            save_path - The newly created folder path.
        """

        curr_folder = os.path.dirname(os.path.realpath(__file__))

        path = os.path.join(curr_folder, 'training_output')

        if not os.path.exists(path):
            os.makedirs(path)

        new_version = self._get_next_folder_num(path)

        save_path = os.path.join(path, f'v{new_version}')

        if create:
            os.makedirs(save_path)

        return save_path

    def _get_next_folder_num(self, path) -> int:
        """ Checks input folder for the next version number: v1, v2, v3 .... vn

        Args:
            path: Path of the output folder.

        Returns:
            an integer indicating the next version number.
        """
        if not os.path.exists(path):
            os.makedirs(path)

        all_folders = [file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))]

        new_version = 1

        if all_folders:
            num_list = [int(folder.replace('v', '')) for folder in all_folders if folder.replace('v', '').isdigit()]
            num_list.sort()
            if num_list:
                new_version = num_list[-1] + 1

        return new_version

##
# @file
#
# @brief Main usage simulation.


if __name__ == '__main__':
    ## Main for training process
    main_class = Main(cfg=config, training_path=None, validation_path=None)  # Example: training_path=os.getcwd() + '/datasets')
    main_class.execute_trainer()

    ## Path to last saved model
    current_folder = os.path.dirname(os.path.realpath(__file__))
    last_model_path = os.path.join(current_folder, 'training_output')
    last_model_path = sorted(Path(last_model_path).rglob('*.ckpt'), key=os.path.getmtime, reverse=True)[0]

    ## Main for testing process
    main_class_test = Main(cfg=config, test_dataset_path=None)  # Example: test_dataset_path=os.getcwd() + '/datasets'
    test_results = main_class_test.execute_test(model_path=last_model_path)
    print('*** test results:\n', test_results)

    ## Main for evaluation process
    main_class_eval = Main(cfg=config, test_dataset_path=None)  # Example: test_dataset_path=os.getcwd() + '/datasets'
    eval_results = main_class_eval.execute_eval()
    print('*** Eval results:\n', eval_results)

    ## The results of the comparison between trained model and existing model evaluation.
    comparison_results = generatedProjectNameComparison(
        test_results=test_results,
        eval_results=eval_results,
        metrics_config=config['metrics']).compare()

    print('comparison_results', comparison_results)

    print("Done !!!")
