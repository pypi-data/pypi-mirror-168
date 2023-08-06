from .wordbank import power_words
from .wordbank import uncommon_words
from .tokenize import tokenize
from .calculate_wordbank_percentage import calculate_wordbank_percentage

def test_calculte_wordbank_percentage():
    power_word = iter(power_words)
    uncommon_word = iter(uncommon_words)

    test_case = tokenize(f'1 {next(uncommon_word)} 3 { next(power_word) } 5 { next(power_word) } 7 8 9 10')

    result = calculate_wordbank_percentage(test_case)

    assert result['power'] == 0.2
    assert result['uncommon'] == 0.1

