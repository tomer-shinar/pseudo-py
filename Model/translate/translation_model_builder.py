from Model.translate.generic_to_generic import *
from Model.translate.pos_tagging import *
from Model.translate import *
import os


class TranslationModeBuilder(AbstractModelBuilder):
    def train(self, data_set, save_to):
        """
        trains the model
        :param data_set: (g2g data set, pos data set)
        :param save_to: path to save the model to
        :return: model
        """
        pos_builder = POSTaggerBuilder()
        g2g_builder = Gen2GenBuilder()
        model = TranslationModel(g2g_builder.train(data_set[0]), pos_builder.train(data_set[1]), path=save_to)
        if save_to:
            model.save(save_to)
        return model

    def train_and_test(self, data_set, to_save=True, save_to=None, k=5):
        pass

    def load(self, location, version=None):
        """
        load the model from location
        :param location: path to model.
        :param version: the version inside the path, if None latest
        :return: the model loaded
        """
        if not version:
            sub_dirs = os.listdir(location)
            v1 = max([d for d in sub_dirs if os.path.isdir(os.path.join(location, d)) and d.isdigit()], key=int)
            sub_dirs = os.listdir(os.path.join(location, str(v1)))
            v2 = max([d for d in sub_dirs if os.path.isdir(os.path.join(location, str(v1), d)) and d.isdigit()],
                     key=int)
            version = (v1, v2)
        g2g_builder = Gen2GenBuilder()
        pos_builder = POSTaggerBuilder()
        return TranslationModel(g2g_builder.load(os.path.join(location, *version, "g2g")),
                                pos_builder.load(os.path.join(location, *version, "pos")), version=version)


