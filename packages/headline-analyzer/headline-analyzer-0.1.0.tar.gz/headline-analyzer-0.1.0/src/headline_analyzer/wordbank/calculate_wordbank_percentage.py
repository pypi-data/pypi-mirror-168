from functools import reduce
from .tokenize import get_tag
from itertools import count


def calculate_wordbank_percentage(tokens: list[tuple[str, str]]):
	"""Calculate the percentage of each word in a list of tokens."""
	length = len(tokens)

	# time complexity (O(len(tokens)))

	countDict: dict[str, int] = {}
	percentDict: dict[str, float] = {}

	for token in tokens:
		tag = get_tag(token)
		if(not(tag in countDict)):
			countDict[tag] = 1
		else:
			countDict[tag] += 1
		percentDict[tag] = countDict[tag]/length

	return percentDict



