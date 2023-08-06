from .count_characters import count_characters

def test_count_characters():
    test_10 = 'x' * 10
    test_1001 = 'x' * 1001
    test_999 = 'x' * 999
    
    assert count_characters(test_10) == 10
    assert count_characters(test_1001)== 1001
    assert count_characters(test_999)== 999