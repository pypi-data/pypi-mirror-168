"""Utilities for checking quality of coordinates

"""
import itertools
import typing
import warnings

import numpy
import pandas
import plotly.express as px

from manifold import metric

ERROR_LABELS = {
	-1: 'Eigenvalue Error',
	-2: 'Max Diff Error',
	-3: 'XLAL Error',
}


class QualityColumn:
	"""Constants for columns"""
	QA = 'qa'
	Label = 'label'


def build_grid(g: metric.Metric, grid_bounds: dict, grid_size: int) -> typing.List[typing.Tuple[float, ...]]:
	grid_bounds = g.coord_func._normalize_coorddict(grid_bounds)
	return list(itertools.product(*[numpy.linspace(grid_bounds[t][0],
												   grid_bounds[t][1],
												   grid_size) for t in g.coord_func.FROM_TYPES]))


def eval_metric(g, grid_point, method: str, target_match: float):
	c = numpy.array(grid_point)
	try:
		m = g.evaluate(c, method=method)
		max_diff = metric.max_diff_at_edges(g, c, m, target_match)
		return max_diff

	except metric.EigenvalueError as e:
		return -1
	except metric.MaxDiffError as e:
		return -2
	except Exception as e:
		# potentially log error
		return -3


def quality_df(g: metric.Metric, grid: typing.List[typing.Tuple[float, ...]], method: str, target_match: float = 0.99):
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		evals = [eval_metric(g, p, method, target_match) for p in grid]

	df = pandas.DataFrame(data=grid, columns=[t.key for t in g.coord_func.FROM_TYPES])
	df[QualityColumn.QA] = evals
	df[QualityColumn.Label] = df[QualityColumn.QA].map(lambda x: ERROR_LABELS.get(x, 'Success'))

	return df


def plot_quality_2d(df: pandas.DataFrame, x: str, y: str, color: str = QualityColumn.Label, height: int = 400, width: int = 400):
	if color not in (QualityColumn.QA, QualityColumn.Label):
		raise ValueError('Unknown color column {}. options are: {}'.format(color, (QualityColumn.QA, QualityColumn.Label)))
	fig = px.scatter(df, x=x, y=y, color=color,
					 title='Coordinate Quality Map',
					 opacity=0.7,
					 height=height, width=width)
	fig.show()
