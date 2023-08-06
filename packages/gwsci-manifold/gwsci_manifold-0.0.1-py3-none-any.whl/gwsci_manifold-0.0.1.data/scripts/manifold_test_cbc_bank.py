#!python
import sys
from optparse import OptionParser

import matplotlib
import numpy

matplotlib.use('agg')

from manifold.utilities import data
from manifold.sources import cbc


def parse_args(args=None):
    if args is None:
        args = sys.argv[1:]
    p = OptionParser(usage="Usage: %prog [options]")

    p.add_option("-n", "--n", type="int", default=10, help="number of simulations to do. default 10")
    p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")
    p.add_option("", "--output-h5", default="test.h5", help="Specify the output h5 file. Default test.h5")

    # assume that the only arg given is a bank
    (opt, args) = p.parse_args(args)
    return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	Bank = cbc.Bank.load(args[0])

	m1s, m2s, s1s, s2s = [], [], [], []
	mismatches = []

	while len(mismatches) < opt.n:
		c = Bank.rectangles[0].metric.coord_func.random()
		if Bank.constraint(c):
			continue
		match = Bank.nearest(c)
		m1s.append(c[cbc.M1])
		m2s.append(c[cbc.M2])
		s1s.append(c[cbc.S1Z])
		s2s.append(c[cbc.S2Z])
		mismatches.append(1.-match)
		print (len(mismatches), match)

	io.h5write(opt.output_h5, {'m1s': numpy.array(m1s), 'm2s':numpy.array(m2s), 's1s':numpy.array(s1s), 's2s': numpy.array(s2s), 'mismatches':numpy.array(mismatches)})

if __name__ == '__main__':
    main()
