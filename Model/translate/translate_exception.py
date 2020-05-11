class TranslationException(Exception):
    """
    class to represent an Error during translation that prevents from translating
    """
    def __init__(self, message):
        Exception.__init__(self, message)
