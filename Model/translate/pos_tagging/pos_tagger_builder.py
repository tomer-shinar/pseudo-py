from Model.translate.pos_tagging import *
from Model.translate import *
from nltk.tag.util import untag
from sklearn_crfsuite import CRF
import pickle


def transform_to_dataset(tagged_sentences):
    """
    transform list of tagged sentences to list of untagged sentences and list of tags
    :param tagged_sentences: list of sentences, each contains tuples of (word, tag)
    :return: list of sentences, list of sentences tags
    """
    X, y = [], []
    for tagged in tagged_sentences:
        X.append([features(untag(tagged), index) for index in range(len(tagged))])
        y.append([tag for _, tag in tagged])
    return X, y


class POSTaggerBuilder(AbstractModelBuilder):
    """
    class that builds POSTagger
    """

    def train(self, data_set, save_to=None):
        """
        train the model and returns it
        :param data_set: tagged sentences
        :param save_to: file to save the file at, if not none
        :return: the model
        """
        model = CRF()
        model.fit(*transform_to_dataset(data_set))
        my_model = POSTagger(model)
        if save_to:
            my_model.save(save_to)
        return my_model

    def train_and_test(self, data_set, to_save=True, save_to=None, k=5):
        raise NotImplemented

    def load(self, location):
        f = open(location + '.pickle', 'rb')
        model = pickle.load(f)
        f.close()
        return POSTagger(model)

