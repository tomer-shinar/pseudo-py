from bidict import bidict
import math
import torch
import json


SOS = "SOS"
EOS = "EOS"
UNK = "UNK"


class Lang:
    """
    language class,
    used to store the vocabulary of each language
    """
    def __init__(self, language):
        self.language_name = language
        self.word_to_index = bidict({})

    def build_language(self, sentences, max_vocab_size=10000):
        """
        build the language by assigning each word an index.
        :param sentences: list of sentences contain the data of the language
        :param max_vocab_size: max number of word in the language
        """
        word_to_count = {SOS: math.inf, EOS: math.inf, UNK: math.inf}
        # SOS - start of sentence, EOS - end of sentence, UNK - unknown word
        for sentence in sentences:
            for word in sentence:
                if word not in word_to_count:
                    word_to_count[word] = 1
                else:
                    word_to_count[word] += 1
        words = sorted(word_to_count.keys(), key=lambda key: word_to_count[key], reverse=True)
        for i in range(min(len(words), max_vocab_size)):
            self.word_to_index[words[i]] = i

    def sentence_to_tensor(self, sentence):
        """
        takes a sentence and make it tensor.
        :param sentence: list of words
        :return: tensor
        """
        indexes = self.to_index(sentence + [EOS])
        return torch.LongTensor(indexes).view(-1).cuda()  # .cuda()

    def to_index(self, sentence):
        """
        replace each word in the sentence with index
        :param sentence: list of words
        :return: list of indexes
        """
        return [word in self.word_to_index.keys() and self.word_to_index[word] or self.word_to_index[UNK]
                for word in sentence]

    def get_vocab_size(self):
        """
        :return: the size of the vocabulary of the language
        """
        return len(self.word_to_index)

    def save(self, file_name):
        f = open(file_name)
        json.dump(self, f, cls=LangEncoder)
        f.close()


class LangEncoder(json.JSONEncoder):
    """
    encoder for Lang
    """
    def default(self, o):
        if isinstance(o, Lang):
            return {"name": o.language_name, "word_to_index": dict(o.word_to_index)}
        else:
            raise TypeError


class LangDecoder(json.JSONDecoder):
    """
    decoder for Lang
    """
    def decode(self, s):
        as_dictionary = super().decode(s)
        lang = Lang(as_dictionary["name"])
        lang.word_to_index = bidict(as_dictionary["word_to_index"])
        return lang


