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
	p.add_option("", "--min-q", type="float", help="minimum q")
	p.add_option("", "--max-q", type="float", help="maximum q.")
	p.add_option("", "--min-ns-mass", type=float, help="minimum mass to consider an NS.")
	p.add_option("", "--max-ns-mass", type=float, help="maximum mass to consider an NS.")
	p.add_option("", "--min-ns-s1z", type=float, help="minimum spin to allow for an NS.")
	p.add_option("", "--max-ns-s1z", type=float, help="maximum spin to allow for an NS.")
	p.add_option("", "--output-h5", help="Specify the output h5 file.")
	p.add_option("", "--hard-cut", action="store_true", help="use a hard cut on the center of the hyperrectangle to define inside")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	(opt, args) = p.parse_args(args)

	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	Bank = cbc.Bank.load(args[0])

	Bank.constraints = {k: numpy.array([getattr(opt, "min_%s" % k.replace("-","_")) if getattr(opt, "min_%s" % k.replace("-","_")) is not None else Bank.constraints[k][0], getattr(opt, "max_%s" % k.replace("-","_")) if getattr(opt, "max_%s" % k.replace("-","_")) is not None else Bank.constraints[k][1]]) for k in Bank.constraints}

	if opt.hard_cut:
		Bank.hardcut()
	else:
		Bank.trim()
	Bank.save(opt.output_h5)


if __name__ == '__main__':
	main()
