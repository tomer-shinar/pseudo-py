from abc import ABC, abstractmethod
import datetime
from ..logs.observable import Observable


class AbstractModel(ABC, Observable):
    """
    abstract class that represent an abstract model.
    each model used in the translation will inherit this class.
    """
    def __init__(self,  accuracy=None, version=None):
        """
        constructor
        :param accuracy: the accuracy of the model
        :param version: the version of the model, if it is a model from file and not new model.
        """
        super().__init__()
        self.version = version
        self.accuracy = accuracy
        self.creation_time = datetime.datetime.now()

    @abstractmethod
    def evaluate(self, input_data):
        """
        abstract class to run the model on input and evaluate the output
        :param input_data: the input the model gets
        :return: the output of running the model
        """
        pass

    @abstractmethod
    def save(self, file_name):
        """
        abstract method for saving the model to file
        :param file_name: file saving to
        """
        pass

    def notify_result(self, input_data, output):
        """
        notify about the evaluation of data.
        :param input_data: the input the model received
        :param output: the output of the model
        """
        self.notify("result", input_data, output)

    def notify_creation(self):
        """
        notify about the creation of the object
        """
        self.notify("created")

