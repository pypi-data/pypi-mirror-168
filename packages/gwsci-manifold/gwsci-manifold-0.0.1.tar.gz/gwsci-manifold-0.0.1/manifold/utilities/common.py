"""General utilities

"""
from typing import Iterable, Dict, Tuple

import numpy


def bounds_from_lists(names: Iterable[str], mins: Iterable[float], maxes: Iterable[float]) -> Dict[str, Tuple[float, float]]:
	"""Utility for zipping a set of minima and maxima into tuples, keyed by a name.

	Args:
		names:
			Iterable[str], a collection of names that correspond to a (min, max) pair
		mins:
			Iterable[float], a collection of minima that correspond to a name in names
		maxes:
			Iterable[float], a collection of maxima that correspond to a name in names

	Returns:
		Dict[str, Tuple[float, float]], a dictionary specifying bounds for each name
	"""
	if not len(names) == len(mins) == len(maxes):
		raise ValueError('Arguments names, mins, maxes must have same lengths, got: {:d}, {:d}, {:d} respectively.'.format(len(names), len(mins), len(maxes)))
	return {n: (mn, mx) for n, mn, mx in zip(names, mins, maxes)}


MetricMatrix = numpy.ndarray
