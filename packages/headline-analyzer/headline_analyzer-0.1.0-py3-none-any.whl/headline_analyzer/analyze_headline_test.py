from .analyze_headline import analyze_headline

def test_analyze_headline():
  test_headlines = [
    'single',
    'this is a test headline',
    'test headline 2',
    'test headline 3 with a lot of words'
  ]
  # assert features
  for test_headline in test_headlines:
    test_result = analyze_headline(test_headline)
    assert test_result['headline'] == test_headline
    assert test_result['stats']['word_count'] == len(test_headline.split())
