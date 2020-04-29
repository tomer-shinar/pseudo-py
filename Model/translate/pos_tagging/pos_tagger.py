from Model.translate import AbstractModel
from Model.translate.pos_tagging import features
import collections
from bidict import bidict
import pickle


class POSTagger(AbstractModel):
    """
    class for pos tagging
    """

    def __init__(self, model, accuracy=None, version=None):
        """
        :param model: CRF model for tagging
        """
        super().__init__(accuracy, version)
        self.model = model

    def save(self, file_name):
        """
        saves the model to pickle file
        :param file_name: the pickle file name
        """
        f = open(file_name + '.pickle', 'wb')
        pickle.dump(self.model, f)
        f.close()

    def evaluate(self, input_data):
        """
        tag each word, and creates bidict of replacements
        :param input_data: untagged sentence.
        :return: bidict of words to replace
        """
        c = collections.Counter()
        replacements = bidict()
        sentence_features = [features(input_data, index) for index in range(len(input_data))]
        for word, tag in zip(input_data, self.model.predict([sentence_features])[0]):
            if tag != "":
                # need to replace
                if word not in replacements.keys():
                    # not been replaced yet
                    replacements[word] = "<{}{}>".format(tag, c[tag])
                    c[tag] += 1
        return replacements
