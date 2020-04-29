from abc import ABC, abstractmethod


class AbstractModelBuilder(ABC):
    """
    abstract class for builder of model.
    """
    @abstractmethod
    def train(self, data_set, save_to):
        """
        train the model over the data set.
        :param data_set: data set used to train
        :param save_to: location to save the model if not none
        :return: the model
        """
        pass

    @abstractmethod
    def train_and_test(self, data_set, to_save=True, save_to=None, k=5):
        """
        train the model and test it with k-fold cross validation
        :param data_set: data set used to train
        :param to_save: if true, saves the model
        :param save_to: location to save the model if needed. if None then default
        :param k: number of folds in the k-folds test
        :return: the model
        """

    @abstractmethod
    def load(self, location):
        """
        load model from file
        :param location: the location of the model in memory
        :return: the loaded model
        """
        pass

