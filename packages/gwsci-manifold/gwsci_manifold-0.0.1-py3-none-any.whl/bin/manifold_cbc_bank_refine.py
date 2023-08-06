#!/usr/bin/env python
import sys
from optparse import OptionParser
import h5py
import numpy

import manifold.utilities.common
import manifold.utilities.data
from manifold import cover
from manifold.sources import cbc


def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")
	p.add_option("", "--output-h5", default="bank.h5", help="Specify the output h5 file. Default bank.h5")
	p.add_option("", "--mm", type="float", default=0.02, help="mismatch radius of sphere. Default = 0.02")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	Bank = cbc.Bank.load(args[0])
	n = 1
	to_check = None
	while True:
		print ("iteration %d to check %s" % (n, "all" if to_check is None else len(to_check)))
		Bank, to_check = Bank.refine(opt.mm, to_check = to_check, verbose = True)
		if len(to_check) == 0:
			break
		n += 1
	Bank.save(opt.output_h5)


if __name__ == '__main__':
	main()
