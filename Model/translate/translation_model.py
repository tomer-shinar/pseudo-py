from Model.translate import *
import os
import re
import autopep8
import ast

CODE_VERSION = 1

TAB = "\t"
SPACES_TAB = " " * 4


class TranslationModel(AbstractModel):
    """
    the class that creates the translation from pseudo code to python code
    """

    def __init__(self, g2g_model, pos_model, accuracy=None, version=None, path="saved-files"):
        if not version:
            version = self.get_version(path)
        super().__init__(accuracy, (CODE_VERSION, version))
        self.g2g_model = g2g_model
        self.pos_model = pos_model

    def evaluate(self, input_data):
        """
        this is the method that translates from pseudo code to python
        :param input_data: pseudo code text
        :return: list of tuples, each containing pseudo command and python translation
        """
        commands = input_data.split("\n")
        translations = []
        for command in commands:
            translations.append([command, self.translate(command)])
            # using list of 2 items instead of tuple to allow use in js
        return translations

    def translate(self, command):
        """
        translates one command to pseudo command(s)
        :param command: pseudo code string
        :return: python code
        """
        original_command = command
        try:
            # remove tabs from the beginning and counts them
            tabs = 0
            while command.startswith(TAB) or command.startswith(SPACES_TAB):
                tabs += 1
                command = command[1 if command.startswith(TAB) else 4:]
            command_parts = self.split_by_strings(command)
            tokens = sum([self.tokenize(part) for part in command_parts], [])  # produce list of tokens
            if not tokens:
                # empty line
                return ""
            replacements = self.pos_model.evaluate(tokens)
            generic_pseudo = [replacements[t] if t in replacements.keys() else t for t in tokens]
            generic_python = self.g2g_model.evaluate(generic_pseudo)
            python_tokens = [replacements.invers[t] if t in replacements.values() else t for t in generic_python]
            python_code = "".join(python_tokens)
            ast.parse(python_code)
            return SPACES_TAB * tabs + autopep8.fix_code(python_code)
        except (TranslationException, SyntaxError):
            return original_command

    @staticmethod
    def split_by_strings(command):
        """
        split the command around all the strings in the command, meaning "", ''
        :param command: pseudo code command
        :return: list of parts of the command and strings in it
        example: 'if x = \'1\' and y = "2" print "hi"' => ['if x = ', '\'1\'', ' and y = ', '"2"', ' print ', '"hi"']
        """
        parts = []
        while command.find('"') != -1 or command.find("'") != -1:
            separator = '"' if command.find("'") == -1 else "'" if command.find('"') == -1 else min('"', "'",
                                                                                                    key=command.find)
            # separator is the firs appears between " and '
            # add the part until the separator
            parts.append(command[:command.find(separator)])
            command = command[command.find(separator) + 1:]
            if command.find(separator) == -1:
                raise TranslationException("found opening {0} without closing one".format(separator))
            parts.append(separator + command[:command.find(separator) + 1])
            command = command[command.find(separator) + 1:]
        parts.append(command)
        return [p for p in parts if p != ""]

    @staticmethod
    def tokenize(sub_command):
        """
        splits the sub command to tokens.
        each token is an independent unit in the command translation
        :param sub_command: part of command
        :return: list of tokens
        """
        if sub_command.startswith("'") or sub_command.startswith('"'):
            # string doesn't need to be tokenize
            return [sub_command]
        token_regex = '|'.join([
            r'([^\W0-9]\w*)',  # name
            r'(\d+\.?\d*)',  # number (without sign)
            r'.'  # any single char
        ])
        return [tok.group() for tok in re.finditer(token_regex, sub_command) if tok.group() != " "]

    def save(self, file_name):
        """
        saves the model at file_name/version
        :param file_name: base directory
        """
        path = os.path.join(file_name, *(str(v) for v in self.version))
        os.mkdir(path)
        self.g2g_model.save(os.path.join(path, "g2g"))
        self.pos_model.save(os.path.join(path, "pos"))

    @staticmethod
    def get_version(path):
        """
        gets the version of this model
        :return: int representing the model version
        """
        if not os.path.isdir(os.path.join(path, str(CODE_VERSION))):
            os.mkdir(os.path.join(path, str(CODE_VERSION)))
            f = open(os.path.join(path, str(CODE_VERSION), "versions.txt"), 'w')
            f.write("1")
            f.close()
            return 0
        f = open(os.path.join(path, str(CODE_VERSION), "versions.txt"), 'r')
        version = int(f.read())
        f.close()
        f = open(os.path.join(path, str(CODE_VERSION), "versions.txt"), 'w')
        f.write(str(version + 1))
        f.close()
        return version
