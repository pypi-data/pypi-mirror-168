#!/usr/bin/env python
import sys
from optparse import OptionParser

import numpy
from lal import series
from ligo.lw import utils as ligolw_utils
from matplotlib import pyplot as plt

import manifold.utilities.data
from manifold import metric
from manifold.sources.cbc import M1M2, CBCMetric


def parse_args(args: list = sys.argv[1:]):
	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("", "--min-m1", type="float", default=1.0, help="Value for m1. Default is 1.0 for m1.")
	p.add_option("", "--min-m2", type="float", default=1.0, help="Value for m2. Default is 1.0 for m2.")
	p.add_option("", "--max-m1", type="float", default=100.0, help="Value for m1. Default is 1.0 for m1.")
	p.add_option("", "--max-m2", type="float", default=100.0, help="Value for m2. Default is 1.0 for m2.")
	p.add_option("", "--num", type="int", default=20, help="number of points. default 20")
	p.add_option("", "--psd-xml", default=(manifold.utilities.data.DATA_ROOT / 'psd_for_treebank.xml.gz').as_posix(), help="Specify the h5 file where the psd is stored.")
	# p.add_option("","--cfunc", help = "specify the coordinate system. Must be in the form of m1_m2_s1z_s2z(bounds).")
	p.add_option("", "--freq_low", type="float", default=10., help="flow of the serach. Default = 10.")
	p.add_option("", "--freq_high", type="float", default=512., help="fhigh of the serach. Default = 512.")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	(opt, args) = p.parse_args(args)
	return opt


def main(args=None, show_plot: bool = True):
	# Uncomment the below to run with specific args
	# args = [
	#
	# ]
	if args is None:
		args = sys.argv[1:]

	opt = parse_args(args)
	coord_func = M1M2(m1=(opt.min_m1, opt.max_m1), m2=(opt.min_m2, opt.max_m2))
	psd = series.read_psd_xmldoc(ligolw_utils.load_filename(opt.psd_xml, verbose=True, contenthandler=series.PSDContentHandler))['H1']
	g = CBCMetric(psd, coord_func, opt.freq_low, opt.freq_high, approximant="IMRPhenomD")

	n = opt.num
	vol = numpy.zeros(n * n)
	for i, (m1, m2) in enumerate(coord_func.grid(m1=n, m2=n)):
		try:
			mt = g([m1, m2])
			vol[i] = numpy.log10(metric.volume_element(mt))
		except Exception as e:
			print(e)

	if show_plot:
		plt.pcolormesh(vol.reshape(n, n))
		plt.colorbar()
		plt.show()
	else:
		return vol


if __name__ == '__main__':
	main()
