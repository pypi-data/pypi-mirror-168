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

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	Bank = cbc.Bank.load(args[0])
	print (Bank.rectangles[0], len(Bank.rectangles))

if __name__ == '__main__':
	main()
