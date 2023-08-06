from typing import Literal
from .power_words import power_words
from .uncommon_words import uncommon_words

def tag_from_wordbanks(word: str) -> Literal['power' , 'uncommon', '']:
  word_lower = word.lower()
  if word_lower in power_words:
    return 'power'
  elif word_lower in uncommon_words:
    return 'uncommon'
  else:
    return ''