"""EAR Dataset Loading

Loading and data processing for EAR Dataset.

Author: Jigar Hira
"""


import os
import numpy as np
from typing import Tuple


class EARDataset:
    """EAR project dataset generation, loading, and attributes.
    
    """

    # dataset parameters
    SAMPLE_CATEGORIES = [0, 1, 2, 3]
    SAMPLE_SHAPE = (128, 259)
    
    TRAINING_FOLDS = 9
    VALIDATION_FOLDS = 1
    SAMPLES_PER_FOLD = 2400

    def __init__(self) -> None:
        # training data
        self.train_x = np.zeros((self.TRAINING_FOLDS, self.SAMPLES_PER_FOLD, self.SAMPLE_SHAPE[0], self.SAMPLE_SHAPE[1]))
        self.train_y = np.zeros((self.TRAINING_FOLDS, self.SAMPLES_PER_FOLD))
        # validation data
        self.test_x = np.zeros((self.VALIDATION_FOLDS, self.SAMPLES_PER_FOLD, self.SAMPLE_SHAPE[0], self.SAMPLE_SHAPE[1]))
        self.test_y = np.zeros((self.VALIDATION_FOLDS, self.SAMPLES_PER_FOLD))


    def load(self, dataset_file_path:str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Loads dataset binaries from file and returns the sample sets.

        Args:
            dataset_file_path (str): folder path to binaries

        Returns:
            np.ndarray, np.ndarray, np.ndarray, np.ndarray: train_x, train_y, test_x, test_y
        """
        # load dataset binaries
        print('Loading dataset files')
        try:
            train_x = np.load(dataset_file_path + 'train_x.npy', allow_pickle=True)
            train_y = np.load(dataset_file_path + 'train_y.npy', allow_pickle=True)
            test_x = np.load(dataset_file_path + 'test_x.npy', allow_pickle=True)
            test_y = np.load(dataset_file_path + 'test_y.npy', allow_pickle=True)
            print('Dataset loading complete')
        except FileNotFoundError as e:
            print('Binaries could not be found in ' + dataset_file_path + '\nRun generate before load\n', e)
            return None, None, None, None

        return train_x, train_y, test_x, test_y
    
    
    def generate(self, training_data_path:str, validation_data_path:str, output_file_path:str):
        """Generates dataset binaries from spectrogram files.

        Args:
            training_data_path (str): folder path to training data
            validation_data_path (str): folder path to validation data
            output_file_path (str): output file path
        """
        count = 0

        print('Loading test set')
        # iterate through all the samples in the training folder
        for root, _, files in os.walk(training_data_path):
            # iterate through all the sample files
            for file in files:
                filepath = root + os.sep + file
                
                # parse sample filename
                sample_num, fold, category = file[:-4].split('-')
                sample_num, fold, category = int(sample_num), int(fold), int(category)

                # load spectrogram
                spectrogram = np.load(filepath, allow_pickle=True)

                # add sample to training sets
                self.train_x[fold][sample_num % self.SAMPLES_PER_FOLD] = spectrogram
                self.train_y[fold][sample_num % self.SAMPLES_PER_FOLD] = category

                count += 1
                if count % 1000 == 0:
                    print('loaded ' + str(count) + ' spectrograms')

        count = 0
        
        print('Loading validation set')
        # iterate through all the samples in the validation folder
        for root, _, files in os.walk(validation_data_path):
            # iterate through all the samples files
            for file in files:
                filepath = root + os.sep + file

                # parse sample filename
                sample_num, fold, category = file[:-4].split('-')
                sample_num, fold, category = int(sample_num), int(fold) - self.TRAINING_FOLDS, int(category)

                # load spectrogram
                spectrogram = np.load(filepath, allow_pickle=True)

                # add sample to validation sets
                self.test_x[fold][sample_num % self.SAMPLES_PER_FOLD] = spectrogram
                self.test_y[fold][sample_num % self.SAMPLES_PER_FOLD] = category

                count += 1
                if count % 1000 == 0:
                    print('loaded ' + str(count) + ' spectrograms')

        # save dataset to numpy arrays
        print('Saving dataset to files')
        np.save(output_file_path + 'train_x.npy', self.train_x, allow_pickle=True)
        np.save(output_file_path + 'train_y.npy', self.train_y, allow_pickle=True)
        np.save(output_file_path + 'test_x.npy', self.test_x, allow_pickle=True)
        np.save(output_file_path + 'test_y.npy', self.test_y, allow_pickle=True)


if __name__ == "__main__":
    dataset = EARDataset()
    dataset.load('.')
