#!/usr/bin/env python
import itertools
import sys
import typing
from optparse import OptionParser

import numpy
import pandas
from lal import series
from ligo.lw import utils as ligolw_utils

import manifold.utilities.data
from manifold import metric, coordinate
from manifold.sources.cbc import M1M2, CBCMetric


def parse_args(args: list = None):
	if args is None:
		args = sys.argv[1:]

	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("", "--min-m1", type="float", default=1.0, help="Value for m1. Default is 1.0 for m1.")
	p.add_option("", "--min-m2", type="float", default=1.0, help="Value for m2. Default is 1.0 for m2.")
	p.add_option("", "--max-m1", type="float", default=100.0, help="Value for m1. Default is 1.0 for m1.")
	p.add_option("", "--max-m2", type="float", default=100.0, help="Value for m2. Default is 1.0 for m2.")

	p.add_option("", "--m1-interval", type="float", default=10.0, help=" m1 interval")
	p.add_option("", "--m2-interval", type="float", default=10.0, help=" m2 interval")

	p.add_option("", "--m1-center", type="float", default=100.0, help=" m1 center")
	p.add_option("", "--m2-center", type="float", default=100.0, help=" m2 center")

	p.add_option("", "--psd-xml", default=(manifold.utilities.data.DATA_ROOT / 'psd_for_treebank.xml.gz').as_posix(), help="Specify the h5 file where the psd is stored.")

	# p.add_option("","--cfunc", help = "specify the coordinate system. Must be in the form of m1_m2_s1z_s2z(bounds).")
	p.add_option("", "--freq_low", type="float", default=10., help="flow of the search. Default = 10.")
	p.add_option("", "--freq_high", type="float", default=512., help="fhigh of the search. Default = 512.")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	(opt, args) = p.parse_args(args)
	return opt


def build_grid(m1_min, m1_max, m1_interval, m2_min, m2_max, m2_interval, dt_min=0, dt_max=0, dt_interval=0):
	return itertools.product(numpy.arange(m1_min, m1_max, m1_interval),
							 numpy.arange(m2_min, m2_max, m2_interval),
							 numpy.arange(dt_min, dt_max, dt_interval))


def match_on_grid(g: metric.Metric, center: coordinate.Coordinates, grid: typing.Iterable[coordinate.Coordinates]):
	w_c = g.waveform(center)
	w_grid = [g.waveform(c[:-1]) for c in grid]

	fft_grid = [g.fft_match(w_c, w) - 1 for w in w_grid]
	mm1_grid = [metric.match_minus_1(w_c, w, g.freq_vec, c[-1]) for w, c in zip(w_grid, grid)]

	res = pandas.DataFrame(grid, columns=[c.key for c in g.coord_func.FROM_TYPES])
	res['fft'] = fft_grid
	res['mm1'] = mm1_grid
	res['diff'] = res['fft'] - res['mm1']
	return res


def metric_match_on_grid(min_m1, max_m1, min_m2, max_m2, psd_xml, freq_low, freq_high, m1_interval, m2_interval, dt_min, dt_max, dt_interval, m1_center, m2_center):
	# Setup CoordFunc
	coord_func = M1M2(m1=(min_m1, max_m1), m2=(min_m2, max_m2))

	# Load PSD
	psd = series.read_psd_xmldoc(ligolw_utils.load_filename(psd_xml, verbose=True, contenthandler=series.PSDContentHandler))['H1']

	# Create Metric
	g = CBCMetric(psd, coord_func, freq_low, freq_high, approximant="IMRPhenomD")

	grid = build_grid(min_m1, max_m1, m1_interval, min_m2, max_m2, m2_interval, dt_min, dt_max, dt_interval)

	c = numpy.array([m1_center, m2_center])

	df = match_on_grid(g, c, grid)
	return df


def main(args=None, show_plot: bool = True):
	if args is None:
		args = parse_args(args)

	df = metric_match_on_grid(args.min_m1, args.max_m1, args.min_m2, args.max_m2, args.psd_xml, args.freq_low, args.freq_high, args.m1_interval, args.m2_interval, args.dt_min,
							  args.dt_max, args.dt_interval, args.m1_center, args.m2_center)

	print(df)


if __name__ == '__main__':
	main()
