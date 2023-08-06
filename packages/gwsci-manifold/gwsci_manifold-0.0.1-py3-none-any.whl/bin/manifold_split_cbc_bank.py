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

	p.add_option("", "--output-left", help="Specify the left output file.")
	p.add_option("", "--output-right", help="Specify the right output file.")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	Bank = cbc.Bank.load(args[0])
	left, right = Bank.split()
	if opt.output_left is not None: left.save(opt.output_left)
	if opt.output_right is not None: right.save(opt.output_right)

if __name__ == '__main__':
	main()
