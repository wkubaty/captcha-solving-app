def load_words(words_path):
    with open(words_path, 'r') as source:
        return [word.replace('\n', '') for word in source.readlines()]
