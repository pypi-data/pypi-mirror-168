from .count_words import count_words
from .count_characters import count_characters

def get_headline_stats(headline: str) -> dict:
  if(type(headline) != str):
    raise TypeError('headline must be a string')

  result = {
    "word_count": count_words(headline), 
    "character_count": count_characters(headline)
  }
  return result
