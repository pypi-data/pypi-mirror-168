#!/usr/bin/env python
import sys
from optparse import OptionParser

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

import manifold.utilities.common
import manifold.utilities.data
from manifold import cover
from manifold.sources import cbc


def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("", "--x", type="int", default=0, help="Set the axis to use for the x coordinate. Default 0")
	p.add_option("", "--y", type="int", default=1, help="Set the axis to use for the y coordinate. Default 1")
	p.add_option("", "--x-scale", default="linear", help="Specify the x-scale. Default linear")
	p.add_option("", "--y-scale", default="linear", help="Specify the y-scale. Default linear")
	p.add_option("", "--output", default="plot.png", help="Specify the output file. Default output.png")
	p.add_option("", "--patches", action="store_true", help="Also plot the patches, can be slow / crash for big banks")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	# assume that the only arg given is a bank
	(opt, args) = p.parse_args(args)
	return opt, args


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt, args = parse_args(args)

	fig = pyplot.figure(figsize=(3.375,3))
	ax = pyplot.gca()
	total_len = 0
	for fn in args:
		Bank = cbc.Bank.load(fn)
		x,y = [], []
		for r in Bank.rectangles:
			if opt.patches:
				p = r.patch(x = opt.x, y = opt.y)
				ax.add_patch(p)
			x.append(r.center[opt.x])
			y.append(r.center[opt.y])
		# FIXME dont hardcode these
		pyplot.scatter(x,y,1)
		print (len(x))
		total_len += len(x)
	pyplot.ylabel("$\log_{10} m_2$")
	pyplot.xlabel("$\log_{10} m_1$")
	ax.set_xscale(opt.x_scale)
	ax.set_yscale(opt.y_scale)
	print (total_len)
	fig.tight_layout()
	pyplot.savefig(opt.output)


if __name__ == '__main__':
	main()
