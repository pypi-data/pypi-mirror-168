from random import random
from .tokenize import tokenize

def test_tokenize():
    test_case = 'this is a headline for testing'
    test_case_words = test_case.split()

    result = tokenize(test_case)

    assert type(result) == list
    assert type(result[0]) == tuple
    assert type(result[0][0]) == str
    assert result[0][0] == test_case_words[0]

    random_index = int(random() * len(test_case_words))
    assert result[random_index][0] == test_case_words[random_index]

    assert result[-1][0] == test_case_words[-1]