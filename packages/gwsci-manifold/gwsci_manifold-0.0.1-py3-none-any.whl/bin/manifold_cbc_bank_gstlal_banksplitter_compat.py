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
	p.add_option("--output-xml", help="set the name of the output xml file")
	p.add_option("--clip-left", action="append", help="set the left templates to clip")
	p.add_option("--clip-right", action="append", help="set the right templates to clip")
	p.add_option("--bank-id", action="append", help="set the bank id")
	p.add_option("--approximant", help="set approximant string")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	Bank = cbc.Bank.load(args[0])
	if opt.verbose: print ("writing %s" % opt.output_xml)
	Bank.to_ligolw(opt.output_xml, "gstlal_bank_splitter", opt.__dict__)

if __name__ == '__main__':
	main()
