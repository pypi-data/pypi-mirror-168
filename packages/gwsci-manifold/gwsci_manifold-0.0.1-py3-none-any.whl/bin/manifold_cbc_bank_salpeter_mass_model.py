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

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	# assume T00517 file name convention and .h5 extension
	infname = args[0]
	ifo, tag, start, dur = infname.replace('.h5','').split('-')

	# load bank, sort and reassign ids to be the sort order
	# NOTE!!! This means that you have to write the bank file back out!!
	Bank = cbc.Bank.load(infname)
	Bank.sort()
	Bank.assign_ids()

	# setup data for the mass model
	p_of_tj_given_alpha = numpy.zeros(len(Bank))
	coords = numpy.zeros((3, len(Bank)))
	cfunc = Bank.rectangles[0].metric.coord_func

	# Assert that we have a log m1 log m2 coord func
	assert cfunc.key == "log10m1_log10m2_chi"

	# First calculate the probability of template j given alpha
	for ix, (ID, r) in enumerate(zip(Bank.ids, Bank.rectangles)):
		assert ix == ID
		coords[:,ix], p_of_tj_given_alpha[ix] = cfunc.salpeter_prob(r)

	coefficients, breakpoints = Bank.prob_of_tk_given_rho(p_of_tj_given_alpha)

	xmlfname = "%s-%s-%s-%s.xml.gz" % (ifo, tag, start, dur)
	massmodelfname = "%s-%s_MASS_MODEL-%s-%s.h5" % (ifo, tag, start, dur)

	# Write it out
	Bank.save(infname)

	f = h5py.File(massmodelfname, "w")
	f.create_dataset("SNR", data = numpy.array(breakpoints))
	f.create_dataset("coefficients", data = coefficients, compression="gzip")
	f.create_dataset("template_id", data = numpy.array(Bank.ids).astype(int))
	f.create_dataset("m1s", data = coords[0,:])
	f.create_dataset("m2s", data = coords[1,:])
	f.create_dataset("chis", data = coords[2,:])
	f.close()



if __name__ == '__main__':
	main()
