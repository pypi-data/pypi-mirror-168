#!python
import sys
from optparse import OptionParser

import matplotlib
import numpy

matplotlib.use('agg')
matplotlib.rcParams.update({
	"font.size": 9.0,
	"axes.titlesize": 9.0,
	"axes.labelsize": 9.0,
	"xtick.labelsize": 9.0,
	"ytick.labelsize": 9.0,
	"legend.fontsize": 8.0,
	"figure.dpi": 300,
	"savefig.dpi": 300,
	"text.usetex": True,
	"path.simplify": True,
	"font.family": "serif"
})



from matplotlib import pyplot

from manifold.utilities import data


def parse_args(args=None):
    if args is None:
        args = sys.argv[1:]
    p = OptionParser(usage="Usage: %prog [options]")

    (opt, args) = p.parse_args(args)
    return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)
	test = io.h5read(args[0])

	mismatches = test['mismatches']
	mismatches[mismatches > 0.05] = 0.05
	ix = numpy.argsort(mismatches)
	mismatches =  mismatches[ix]
	m1s = test['m1s'][ix]
	m2s = test['m2s'][ix]
	s1s = test['s1s'][ix]
	s2s = test['s2s'][ix]
	chis = (m1s * s1s + m2s * s2s) / (m1s + m2s)
	fig = pyplot.figure(figsize=(7,2.5))
	pyplot.subplot(131)
	pyplot.scatter(m1s, m2s, c=mismatches, s=2)
	ax = pyplot.gca()
	pyplot.xlabel('m1')
	pyplot.ylabel('m2')
	ax.set_yscale('log')
	ax.set_xscale('log')
	pyplot.colorbar()
	pyplot.subplot(132)
	pyplot.scatter(m1s, chis, c=mismatches, s=2)
	ax = pyplot.gca()
	pyplot.xlabel('m1')
	pyplot.ylabel('chi')
	ax.set_yscale('linear')
	ax.set_xscale('log')
	pyplot.colorbar()
	pyplot.subplot(133)
	mismatches.sort()
	percent = numpy.arange(1, len(mismatches)+1) / len(mismatches)
	mm50 = mismatches[numpy.searchsorted(percent, 0.50)]
	mm90 = mismatches[numpy.searchsorted(percent, 0.90)]
	mm99 = mismatches[numpy.searchsorted(percent, 0.99)]
	mm999 = mismatches[numpy.searchsorted(percent, 0.999)]
	pyplot.plot(mismatches, numpy.arange(len(mismatches)) / len(mismatches))
	pyplot.text(mm50-.004,0,'50\%',rotation=90)
	pyplot.vlines(mm50, 0, 1)
	pyplot.text(mm90-.004,0,'90\%',rotation=90)
	pyplot.vlines(mm90, 0, 1)
	pyplot.text(mm99-.004,0,'99\%',rotation=90)
	pyplot.vlines(mm99, 0, 1)
	pyplot.text(mm999-.004,0,'99.9\%',rotation=90)
	pyplot.vlines(mm999, 0, 1)
	#pyplot.hist(mismatches, 25, cumulative=True)
	pyplot.xlabel('mismatch')
	pyplot.ylabel('fraction')
	fig.tight_layout()
	pyplot.savefig(args[0].replace('.h5','.png'))

if __name__ == '__main__':
    main()
