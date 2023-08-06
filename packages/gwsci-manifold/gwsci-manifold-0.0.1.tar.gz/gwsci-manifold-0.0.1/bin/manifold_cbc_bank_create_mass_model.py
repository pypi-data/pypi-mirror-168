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
	p.add_option("--num-groups", type="int", help="number of groups to split")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	Bank = cbc.Bank.load(args[0])
	if opt.num_groups is None: opt.num_groups = len(Bank.rectangles)
	for i, bank in enumerate(Bank.group(opt.num_groups)):
		ifo, tag, start, dur = args[0].replace(".h5", "").split('-')
		fname = "%s-%05d_%s-%s-%s.h5" % (ifo, i, tag, start, dur)
		bank.save(fname)

if __name__ == '__main__':
	main()
