from .infer import infer_headline_stats

def test_infer_headline_stats():
  test_case_high = {'word_count': 18, 'headline': 'test headline 1'}
  test_case_low = {'word_count': 2, 'headline': 'test headline 2'}
  test_case_optimal = {'word_count': 9, 'headline': 'test headline 3'}

  # assertions
  result_high = infer_headline_stats(test_case_high)
  assert result_high['word_count_inference'] == 'high'

  result_low = infer_headline_stats(test_case_low)
  assert result_low['word_count_inference'] == 'low'
  assert result_low['word_count_message'] == 'word count is too low'

  result_optimal = infer_headline_stats(test_case_optimal)
  assert result_optimal['word_count_inference'] == 'optimal'