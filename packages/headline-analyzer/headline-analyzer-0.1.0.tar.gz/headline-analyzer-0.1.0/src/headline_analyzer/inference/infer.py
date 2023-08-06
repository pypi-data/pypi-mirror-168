def infer_headline_stats(headlines_stats: dict) -> dict:
  """Infer headline stats from a list of headlines stats."""
  # Infer word count
  word_count_message = 'word count is optimal'
  word_count_inference = 'optimal'

  if headlines_stats['word_count'] < 4:
    word_count_message = 'word count is too low'
    word_count_inference = 'low'
  elif headlines_stats['word_count'] > 15:
    word_count_message = 'word count is too high'
    word_count_inference = 'high'

  result = {
    'word_count_message': word_count_message,
    'word_count_inference': word_count_inference
  }

  return result