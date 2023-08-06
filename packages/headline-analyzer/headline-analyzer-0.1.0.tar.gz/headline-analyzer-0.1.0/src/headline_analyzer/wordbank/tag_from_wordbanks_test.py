from .tag_from_wordbanks import tag_from_wordbanks

def test_tag_from_wordbanks():
    test_case = 'best'

    result = tag_from_wordbanks(test_case)
    assert result == 'power'