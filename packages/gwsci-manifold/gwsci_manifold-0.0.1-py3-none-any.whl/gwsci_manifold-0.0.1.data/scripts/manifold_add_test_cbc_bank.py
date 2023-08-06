#!python
import sys
from optparse import OptionParser
import bisect

import numpy
	
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot

import manifold.utilities.common
import manifold.utilities.data
from manifold import cover
from manifold.sources import cbc
from manifold import io

def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")
	p.add_option("", "--output-h5", default="test.h5", help="Specify the output h5 file. Default test.h5")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	m1s, m2s, s1s, s2s = [], [], [], []
	mismatches = []

	for arg in args:
		t = io.h5read(arg)
		m1s.extend(numpy.array(t['m1s']))
		m2s.extend(numpy.array(t['m2s']))
		s1s.extend(numpy.array(t['s1s']))
		s2s.extend(numpy.array(t['s2s']))
		mismatches.extend(numpy.array(t['mismatches']))
       
	io.h5write(opt.output_h5, {'m1s': numpy.array(m1s), 'm2s':numpy.array(m2s), 's1s':numpy.array(s1s), 's2s': numpy.array(s2s), 'mismatches':numpy.array(mismatches)})

if __name__ == '__main__':
	main()
