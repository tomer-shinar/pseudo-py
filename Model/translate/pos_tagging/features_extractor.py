def features(sentence, index):
    """
    extracting features of word at index location inside sentence
    :param sentence: [w1, w2, ...]
    :param index: the index of the word
    :return: dict of features
    """
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'prev_prev_word': '' if index <= 1 else sentence[index - 2],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'next_next_word': '' if index >= len(sentence) - 2 else sentence[index + 2],
        'has_': '_' in sentence[index],
        'is_numeric': sentence[index].replace('.', '', 1).isdigit(),  # check if int or float
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:],
        'is_identifier': sentence[index].isidentifier(),
    }
