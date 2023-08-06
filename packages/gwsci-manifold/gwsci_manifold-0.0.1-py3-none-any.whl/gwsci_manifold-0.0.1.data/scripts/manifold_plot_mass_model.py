#!python
import sys
from optparse import OptionParser
from gstlal.stats.inspiral_intrinsics import SourcePopulationModel

import numpy
	
import matplotlib
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

from manifold import io

def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")

	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	model = io.h5read(args[0])
	ids = numpy.array(model['template_id'])
	m1s = numpy.array(model['m1s'])
	m2s = numpy.array(model['m2s'])
	popmodel = SourcePopulationModel(ids, args[0])

	coeffs = numpy.array([popmodel.lnP_template_signal(tid, 100) for tid in ids])
	ix = coeffs.argsort()
	m1s = m1s[ix]
	m2s = m2s[ix]
	coeffs = coeffs[ix]

	fig = pyplot.figure()
	pyplot.scatter(m1s, m2s, c=coeffs, s=2)
	ax = pyplot.gca()
	pyplot.xlabel('m1')
	pyplot.ylabel('m2')
	ax.set_yscale('log')
	ax.set_xscale('log')
	pyplot.colorbar()
	fig.tight_layout()
	pyplot.savefig(args[0].replace('.h5','.png'))

if __name__ == '__main__':
	main()
