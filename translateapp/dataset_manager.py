import collections
import json

from .models import G2GSuggestion, PosSuggestion
from django.db import models
from Model.translate import *
import ast


class DataSetManager:
    """
    class to manage the data sets for the translation model.
    implements the facade design pattern
    """
    @staticmethod
    def load_g2g_dataset():
        """
        loads the dataset of the g2g
        :return: list of tuples (generic pseudo, generic python, weight)
        """
        samples = G2GSuggestion.objects.all()
        return [obj.get_sample() for obj in samples if obj.to_consider()]

    @staticmethod
    def load_pos_dataset():
        """
        loads the dataset of the pos tagger
        :return: list of tuples (list of tuples (token, pos) weight)
        """
        samples = PosSuggestion.objects.all()
        return [obj.get_sample() for obj in samples if obj.to_consider()]

    @staticmethod
    def suggest(origin, suggestion, user):
        """
        save a suggestion from user to the database
        :param origin: the translation created by the model (user down votes it)
        :param suggestion: the new translation suggested by the user
        :param user: the user suggested
        """
        origin = [t for t in origin if t[0] != '']
        for (pseudo1, down_python), (pseudo2, up_python) in zip(origin, suggestion):
            pseudo1 = pseudo1.strip(" ")
            pseudo2 = pseudo1.strip(" ")
            up_python = remove_tabs(up_python)
            down_python = remove_tabs(down_python)

            if pseudo1 != pseudo2 or not TranslationModel.is_valid(up_python):  # wrong input
                continue
            if down_python == up_python: # user liked the translation
                DataSetManager.up_vote(pseudo1, up_python, user)
            else:  # user didn't like the translation
                # the down is first in case that there is good part in the down_python
                DataSetManager.down_vote(pseudo1, down_python, up_python, user)
                DataSetManager.up_vote(pseudo1, up_python, user, user_suggestion=True)

    @staticmethod
    def up_vote(pseudo, python, voter, user_suggestion=False):
        """
        up vote a translation, if doesn't exist, add it
        :param pseudo: the pseudo code
        :param python: the python code
        :param voter: the user voting
        :param user_suggestion: true if the user suggested it
        """
        generic_pseudo, generic_python, pos_sample = DataSetManager.get_samples(pseudo, python, python)
        existing_sample = PosSuggestion.objects.filter(data=pos_sample)
        if existing_sample:  # found such sample
            existing_sample.do_up_vote(voter)
        else:  # no such sample
            if user_suggestion:
                sample = PosSuggestion(data=pos_sample, suggester=voter)
            else:
                sample = PosSuggestion(data=pos_sample)
            sample.save()

        existing_sample = PosSuggestion.objects.filter(models.Q(gen_python=generic_python) &
                                                       models.Q(gen_pseudo=generic_pseudo))
        if existing_sample:  # found such sample
            existing_sample.do_up_vote(voter)
        else:  # no such sample
            if user_suggestion:
                sample = G2GSuggestion(gen_python=generic_python, gen_pseudo=generic_pseudo, suggester=voter)
            else:
                sample = G2GSuggestion(gen_python=generic_python, gen_pseudo=generic_pseudo)
            sample.save()

    @staticmethod
    def down_vote(pseudo, python, good_python, voter):
        """
        down vote a translation
        :param pseudo: pseudo code
        :param python: python code
        :param good_python: the good translation
        :param voter: the user voting
        """
        generic_pseudo, generic_python, pos_sample = DataSetManager.get_samples(pseudo, python, good_python)
        existing_sample = PosSuggestion.objects.filter(data=pos_sample)
        if existing_sample:  # found such sample
            existing_sample.do_down_vote(voter)

        existing_sample = PosSuggestion.objects.filter(models.Q(gen_python=generic_python) &
                                                       models.Q(gen_pseudo=generic_pseudo))
        if existing_sample:  # found such sample
            existing_sample.do_down_vote(voter)


    @staticmethod
    def extract_pos(python, pseudo):
        """
        extract pos tagging for
        :param python: python code to extract from.
        :param pseudo: pseudo code, only extracting symbols from this
        :return: dict of tags
        """
        def tagger(node):
            """
            for each tag return the word and tag
            """
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.Call):
                return node.name, "func"
            if isinstance(node, ast.Str):
                return node.s, "str"
            if isinstance(node, ast.Num):
                return node.n, "num"
            if isinstance(node, ast.Name):
                return node.id, "name"
            if isinstance(node, ast.NameConstant):
                return node.value, "const"
            if isinstance(node, ast.ClassDef):
                return node.name, "class"
            return None, None

        try:
            root = ast.parse(python)
        except SyntaxError:
            root = ast.parse(python + "\n    pass")  # will work because is valid
        tags = {}
        for node in ast.walk(root):
            word, tag = tagger(node)
            if word and word in pseudo:
                tags[word] = tag
        return tags

    @staticmethod
    def get_samples(pseudo, python, good_python):
        """
        take pseudo python pair and return the samples for the data sets
        :param pseudo: pseudo code
        :param python: python code
        :param good_python: the correct translation to python (can be python but doesn't have to)
        :return: generic pseudo, generic python, pos sample
        """
        pos_tags = DataSetManager.extract_pos(good_python, pseudo)
        python = TranslationModel.tokenize(sum([TranslationModel.tokenize(part) for part in
                                                TranslationModel.split_by_strings(python)], []))
        pseudo = TranslationModel.tokenize(sum([TranslationModel.tokenize(part) for part in
                                                TranslationModel.split_by_strings(pseudo)], []))
        pos_sample = [(tok, pos_tags[tok] if tok in pos_tags.keys() else "") for tok in pseudo]
        c = collections.Counter()
        replacements = {}
        for word, tag in pos_tags.items():
            if tag != "":
                # need to replace
                if word not in replacements.keys():
                    # not been replaced yet
                    replacements[word] = "<{}{}>".format(tag, c[tag])
                    c[tag] += 1
        pseudo = [replacements[tok] if tok in replacements.keys() else tok for tok in pseudo]
        python = [replacements[tok] if tok in replacements.keys() else tok for tok in python]
        return pseudo, python, json.dumps(pos_sample)


def remove_tabs(code):
    """
    remove the same amount of tabs from each line
    :param code:
    :return: the new code
    """
    lines = code.split("\n")
    tabs = count_on_start(lines[0], TAB)
    return [line[tabs*4:] for line in lines]

