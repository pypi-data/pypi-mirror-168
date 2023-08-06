#!python
import sys
from optparse import OptionParser

import numpy

import manifold.utilities.common
import manifold.utilities.data
from manifold import cover
from manifold.sources import cbc

def M_from_mc_q(mc, q):
	return mc / (q / (1.+q)**2)**.6

def m1_from_M_q(M, q):
	return M / (1. + 1. / q)

def m2_from_M_q(M, q):
	return M / (1. + q)

def min_max_M_from_mcs_qs(mcs, qs):
	M = []
	for mc in mcs:
		for q in qs:
			M.append(M_from_mc_q(mc, q))
	return min(M), max(M)

def min_max_m1_from_Ms_qs(Ms, qs):
	m1 = []
	for M in Ms:
		for q in qs:
			m1.append(m1_from_M_q(M, q))
	return min(m1), max(m1)

def min_max_m2_from_Ms_qs(Ms, qs):
	m2 = []
	for M in Ms:
		for q in qs:
			m2.append(m2_from_M_q(M, q))
	return min(m2), max(m2)

def min_max_mi_from_Ms_qs(Ms,qs):
	mnm1,mxm1 = min_max_m1_from_Ms_qs(Ms, qs)
	mnm2,mxm2 = min_max_m2_from_Ms_qs(Ms, qs)
	return round(0.98 * min(mnm1,mxm1,mnm2,mxm2), 2), round(1.02 * max(mnm1,mxm1,mnm2,mxm2), 2)

#
# FIXME NOTE Placement for spin distributions that are not centered on zero is
# broken due to some faulty logic in the placement code. For now, this program
# requires symmetric spin distributions about zero.
#

def parse_args(args=None):
	if args is None:
		args = sys.argv[1:]
	p = OptionParser(usage="Usage: %prog [options]")

	#p.add_option("", "--min-m1", type="float", help="min value for m1.")
	#p.add_option("", "--max-m1", type="float", help="max value for m1.")
	p.add_option("", "--min-m2", type="float", help="min value for m2.")
	#p.add_option("", "--max-m2", type="float", help="max value for m2.")
	#p.add_option("", "--min-chi", default=0., type="float", help="min value for chi. Default 0")
	#p.add_option("", "--max-chi", default=0., type="float", help="max value for chi. Default 0")
	p.add_option("", "--max-abs-chi", default=0., type="float", help="max value for abs chi. Default 0")
	p.add_option("", "--min-mc", type="float", default=0.87, help="minimum chirp mass. default 0.87")
	p.add_option("", "--max-mc", type="float", default=87.0, help="maximum chirp mass. default 87")
	#p.add_option("", "--min-M", type="float", default=0., help="minimum total mass. default 0")
	p.add_option("", "--max-M", type="float", help="maximum total mass.")
	p.add_option("", "--min-q", type="float",  default=1., help="minimum q. default 1")
	p.add_option("", "--max-q", type="float",  default=100., help="maximum q. default 100")
	p.add_option("", "--min-ns-mass", type=float, default=0.0, help="minimum mass to consider an NS. default 0")
	p.add_option("", "--max-ns-mass", type=float, default=3.0, help="maximum mass to consider an NS. default 3.0")
	#p.add_option("", "--min-ns-s1z", type=float, default=-0.05, help="minimum spin to allow for an NS. default -0.05")
	#p.add_option("", "--max-ns-s1z", type=float, default=0.05, help="maximum spin to allow for an NS. default 0.05")
	p.add_option("", "--max-ns-abs-s1z", type=float, default=0.05, help="maximum abs z spin to allow for an NS. default 0.05")
	p.add_option("", "--psd-xml", default=(manifold.utilities.data.DATA_ROOT / 'psd_for_treebank.xml.gz').as_posix(), help="Specify the xml file where the psd is stored.")
	p.add_option("", "--approximant", default="IMRPhenomD", help="Specify either IMRPhenomD or TaylorF2.")
	p.add_option("", "--instrument", default="H1", help="Specify which instrument the bank is for. Default H1")
	p.add_option("", "--freq-low", type="float", default=15., help="flow of the serach. Default = 15.")
	p.add_option("", "--freq-high", type="float", default=512., help="fhigh of the search. Default = 512.")
	p.add_option("", "--max-duration", type="float", default=numpy.inf, help="fhigh of the search. Maximum waveform duration. Default: infinity")
	p.add_option("", "--mm", type="float", default=0.02, help="mismatch radius of sphere. Default = 0.02")
	p.add_option("", "--reuse-g-mm", type="float", default = 0.0, help = "mismatch radius of sphere to reuse the metric. Default 0.0")
	p.add_option("", "--output-xml", default="bank.xml.gz", help="Specify the output ligolw xml file. Default bank.xml.gz")
	p.add_option("", "--output-h5", default="bank.h5", help="Specify the output h5 file. Default bank.h5")
	#p.add_option("", "--aspect-ratio", action="append", type="float", help="set the aspect ratio for each dimension to split one - default 1. Should either not be provided or be provided dimension number of times")
	p.add_option("", "--min-coord-vol", type="float", help="set the minimum coordinate volume. default = infinity", default=numpy.inf)
	p.add_option("", "--max-num-templates", type="float", help="set the maximum number of templates per cell. Default 1", default=1)
	p.add_option("", "--seed-bank", help="set the seed bank. Must contain exactly one rectangle at this time")
	p.add_option("--no-trim", action="store_true", help="Do not trim final result")
	p.add_option("-v", "--verbose", action="store_true", help="Be verbose.")

	(opt, args) = p.parse_args(args)

	opt.min_M, max_M = min_max_M_from_mcs_qs([opt.min_mc, opt.max_mc], [opt.min_q, opt.max_q])
	if opt.max_M is  None:
		opt.max_M = max_M
	opt.min_m1, opt.max_m1 = min_max_mi_from_Ms_qs([opt.min_M, opt.max_M],[opt.min_q, opt.max_q])
	if not opt.min_m2:
		opt.min_m2,  opt.max_m2 = min_max_mi_from_Ms_qs([opt.min_M, opt.max_M],[opt.min_q, opt.max_q])
	else:
		opt.max_m2 = opt.max_m1

	return opt


def main(args=None, show_plot: bool = True, verbose: bool = True):
	opt = parse_args(args)
	#if opt.min_chi==0. and opt.max_chi==0.:
	if opt.max_abs_chi==0.:
		cfunc = cbc.coord_funcs['log10m1_log10m2'](**manifold.utilities.common.bounds_from_lists(['m1', 'm2',], [.95*opt.min_m1, .95*opt.min_m2], [1.1*opt.max_m1, 1.1*opt.max_m2]))
		aspect_ratios = numpy.array([1., 1.])
	else:
		# FIXME don't hardcode this boundary padding
		#cfunc = cbc.coord_funcs['log10m1_log10m2_chi'](**manifold.utilities.common.bounds_from_lists(['m1', 'm2', 'S1z', 'S2z'], [.5*opt.min_m1, .5*opt.min_m2, max(-1, opt.min_chi - .1), max(-1, opt.min_chi - .1)], [2*opt.max_m1, 2*opt.max_m2, min(1., opt.max_chi + .1), min(1., opt.max_chi + .1)]))
		cfunc = cbc.coord_funcs['log10m1_log10m2_chi'](**manifold.utilities.common.bounds_from_lists(['m1', 'm2', 'S1z', 'S2z'], [.5*opt.min_m1, .5*opt.min_m2, max(-1, -opt.max_abs_chi - .1), max(-1, -opt.max_abs_chi - .1)], [2*opt.max_m1, 2*opt.max_m2, min(1., opt.max_abs_chi + .1), min(1., opt.max_abs_chi + .1)]))
		aspect_ratios = numpy.array([1., 1., 4.])

	g = cbc.CBCMetric(manifold.utilities.data.read_psd(opt.psd_xml, opt.instrument, verbose=verbose,),
					  cfunc,
					  opt.freq_low,
					  opt.freq_high,
				 	  max_duration = opt.max_duration,
					  approximant=opt.approximant)

	if opt.seed_bank is not None:
		seedbank = cbc.Bank.load(opt.seed_bank)
		# FIXME add some other checks
		assert len(seedbank.rectangles) == 1
		R = cbc.ManifoldRectangle(seedbank.rectangles[0].mins, seedbank.rectangles[0].maxes, g)
		min_depth = 11#numpy.inf
	else:
		R = cbc.ManifoldRectangle(g.coord_func.mins, g.coord_func.maxes, g)
		min_depth = 11
	C = cbc.Chart(R)

	constraints = {'M': numpy.array([opt.min_M, opt.max_M]),
                       'mc': numpy.array([opt.min_mc, opt.max_mc]),
                       'q':numpy.array([opt.min_q, opt.max_q]),
                       #'chi':numpy.array([opt.min_chi, opt.max_chi]),
                       'chi':numpy.array([-opt.max_abs_chi, opt.max_abs_chi]),
                       'm1': numpy.array([opt.min_m1, opt.max_m1]),
                       'm2': numpy.array([opt.min_m2, opt.max_m2]),
                       'ns-mass': numpy.array([opt.min_ns_mass, opt.max_ns_mass]),
                       #'ns-s1z': numpy.array([opt.min_ns_s1z, opt.max_ns_s1z])
                       'ns-s1z': numpy.array([-opt.max_ns_abs_s1z, opt.max_ns_abs_s1z])
                      }

	def m1c(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.m1_constraint(constraints, cfunc(numpy.array(v)))
	def m2c(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.m2_constraint(constraints, cfunc(numpy.array(v)))
	def Mc(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.M_constraint(constraints, cfunc(numpy.array(v)))
	def mcc(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.mc_constraint(constraints, cfunc(numpy.array(v)))
	def qc(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.q_constraint(constraints, cfunc(numpy.array(v)))
	def chic(v, constraints = constraints, cfunc = cfunc):
		return cbc.Bank.chi_constraint(constraints, cfunc(numpy.array(v)))
	constraint_funcs = [m1c, m2c, Mc, mcc, qc, chic]

	C.branch(mm=opt.mm, reuse_g_mm=opt.reuse_g_mm, constraints=constraint_funcs, verbose=True, aspect_ratios = aspect_ratios, min_coord_vol = opt.min_coord_vol, max_num_templates = opt.max_num_templates, min_depth = min_depth)

	Bank = cbc.Bank.fromChart(C, constraints = constraints)
	if not opt.no_trim: Bank.trim()
	Bank.save(opt.output_h5)


if __name__ == '__main__':
	main()
