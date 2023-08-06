#!/usr/bin/env python
import sys
from optparse import OptionParser

import numpy

import manifold.utilities.common
import manifold.utilities.data
from manifold import cover
from manifold.sources import cbc

def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("", "--min-m1", type="float", help="min value for m1.")
	p.add_option("", "--max-m1", type="float", help="max value for m1.")
	p.add_option("", "--min-m2", type="float", help="min value for m2.")
	p.add_option("", "--max-m2", type="float", help="max value for m2.")
	p.add_option("", "--min-chi", type="float", help="min value for chi.")
	p.add_option("", "--max-chi", type="float", help="max value for chi.")
	p.add_option("", "--min-mc", type="float", help="minimum chirp mass.")
	p.add_option("", "--max-mc", type="float", help="maximum chirp mass.")
	p.add_option("", "--min-M", type="float", help="minimum total mass.")
	p.add_option("", "--max-M", type="float", help="maximum total mass.")
	p.add_option("", "--min-q", type="float", help="minimum q.")
	p.add_option("", "--max-q", type="float", help="maximum q.")
	p.add_option("", "--min-ns-mass", type=float, help="minimum mass to consider an NS.")
	p.add_option("", "--max-ns-mass", type=float, help="maximum mass to consider an NS.")
	p.add_option("", "--min-ns-s1z", type=float, help="minimum spin to allow for an NS.")
	p.add_option("", "--max-ns-s1z", type=float, help="maximum spin to allow for an NS.")
	p.add_option("", "--output-xml", help="Specify the output ligolw xml file.")
	p.add_option("", "--output-h5", help="Specify the output h5 file.")
	p.add_option("--trim", action="store_true", help="Trim bank according to constraints.")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	(opt, args) = p.parse_args(args)

	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	Bank = cbc.Bank.load(args[0])

	nc = Bank.constraints.copy()
	for c in ("M", "mc", "q", "chi", "m1", "m2", "ns-mass", "ns-s1z"):
		mn = getattr(opt, "min_%s" % c.replace("-","_"))
		mx = getattr(opt, "max_%s" % c.replace("-","_"))
		mn = nc[c][0] if mn is None else mn
		mx = nc[c][1] if mx is None else mx
		nc[c] = numpy.array([mn, mx])
	Bank.constraints = nc
	if opt.trim: Bank.trim()
	Bank.save(opt.output_h5)


if __name__ == '__main__':
	main()
