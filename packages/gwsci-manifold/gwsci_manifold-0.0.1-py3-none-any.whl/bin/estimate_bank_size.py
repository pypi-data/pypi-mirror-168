#!/usr/bin/env python3
"""
To run this script:

source env.sh

python3 setup.py install --prefix=/ligo/software/ligo.org/shio.sakon/builds/20210727/opt

./num_of_temp_Log10M1Log10M2Chi --m1-length 1.0 --m2-length 1.0 --s1z-length 1.0 --s2z-length 1.0 --chi-length 1.0 --min-m1 1.0 --max-m1 100 --min-m2 1.0 --max-m2 100 --min-s1z -1.0 --max-s1z 1.0 --min-s2z -1.0 --max-s2z 1.0 --min-chi -1.0 --max-chi 1.0 --psd-h5-file H1L1V1-MASS_ALL-1238206225-100.h5 --duration 0.25 --flow 15. --fhigh 512. --mis-match .03 --total-mass 100. --min-mass-ratio 0.02 --max-mass-ratio 1.0

Change the condition for total mass if the total mass must be smaller than the value given in the option.
"""
import os
import sys
from optparse import OptionParser

import numpy

from manifold import metric, cover
from manifold.sources import cbc
from manifold.utilities import data


def parse_args(args: list = None):
	if args is None:
		args = sys.argv[1:]

	p = OptionParser(usage="Usage: %prog [options]")

	p.add_option("", "--m1-size", type="int", default=None, help="size of the cell m1 in linear. Default is None.")
	p.add_option("", "--m2-size", type="int", default=None, help="size of the cell m2 in linear. Default is None.")
	p.add_option("", "--chi-size", type="int", default=None, help="size of the cell chi in linear. Default is None.")
	p.add_option("", "--min-m1", type="float", default=None, help="min value for m1. Default is None.")
	p.add_option("", "--max-m1", type="float", default=None, help="max value for m1. Default is None.")
	p.add_option("", "--min-m2", type="float", default=None, help="min value for m2. Default is None.")
	p.add_option("", "--max-m2", type="float", default=None, help="max value for m2. Default is None.")
	p.add_option("", "--min-chi", type="float", default=None, help="min value for chi. Default is None.")
	p.add_option("", "--max-chi", type="float", default=None, help="max value for chi. Default is None.")
	p.add_option("", "--spin", type="int", default=0, help="if 1 then use spin")
	p.add_option("", "--method", type="str", default=metric.EvaluationMethod.Deterministic, help="evaluation method")
	p.add_option("", "--psd-xml-gz", help="Specify the xml.gz file where the psd is stored.")
	p.add_option("", "--mm", type="float", default=0.03, help="mm of the search. Default is 0.03")
	p.add_option("", "--flow", type="float", default=10., help="flow of the serach. Default is 10")
	p.add_option("", "--fhigh", type="float", default=512., help="fhigh of the serach. Default is 512")

	(opt, args) = p.parse_args(args=args)
	return opt


def compute_bank_size(g: metric.Metric, min_m1: float, max_m1: float, m1_size: int, min_m2: float, max_m2: float, m2_size: int,
					  min_chi: float = None, max_chi: float = None, chi_size: int = None,
					  spin: bool = False, method: str = metric.EvaluationMethod.Deterministic, mm: float = 0.03):
	def rnd(x, p=2):
		return round(x, p)

	m1s = numpy.linspace(min_m1, max_m1, m1_size)
	m2s = numpy.linspace(min_m2, max_m2, m2_size)
	dm1s = numpy.diff(m1s)
	dm2s = numpy.diff(m2s)
	m1s = m1s[:-1] + dm1s / 2.
	m2s = m2s[:-1] + dm2s / 2.

	if spin:
		chis = numpy.linspace(min_chi, max_chi, chi_size)
		dchis = numpy.diff(chis)
		chis = chis[:-1] + dchis / 2.
		vtmp = cover.tmpvol(mm, 3)
	else:
		vtmp = cover.tmpvol(mm, 2)

	vol = 0.

	for i, (m1, dm1) in enumerate(zip(m1s, dm1s)):
		for j, (m2, dm2) in enumerate(zip(m2s, dm2s)):
			if m2 > m1: break
			c = [m1, m2]
			try:
				if not spin:
					c = g.coord_func({"m1":m1, "m2":m2}, inv=True)
					# jacobian = 1
					jacobian = numpy.log10(numpy.exp(1)) ** 2 / m1 / m2
					vol += metric.volume_element(g.evaluate(c, method=method)) * dm1 * dm2 * jacobian
					print('Vol update', int(vol / vtmp), rnd(m1), rnd(m2))
				else:
					for k, (chi, dchi), in enumerate(zip(chis, dchis)):
						c = g.coord_func({"m1":m1, "m2":m2, "S1z":chi, "S2z":chi}, inv=True)
						jacobian = numpy.log10(numpy.exp(1)) ** 2 / m1 / m2
						vol += metric.volume_element(g.evaluate(c, method=method)) * dm1 * dm2 * dchi * jacobian
						print('Vol update', int(vol / vtmp), rnd(m1), rnd(m2))
			except metric.EvaluationError as e:
				print(c, e)


def main(args: list = None):
	# TODO figure out where this env setting can be generalized
	print('Setting env variable OMP_NUM_THREADS = {:d}'.format(1))
	os.environ["OMP_NUM_THREADS"] = "1"

	args = parse_args(args)

	cf = cbc.Log10M1Log10M2
	bounds = {
		cbc.M1.key: (.1, 1000.),
		cbc.M2.key: (.1, 1000.),
	}
	if args.spin:
		cf = cbc.Log10M1Log10M2Chi
		bounds[cbc.S1Z.key] = (-1.0, 1.0)
		bounds[cbc.S2Z.key] = (-1.0, 1.0)

	g = cbc.CBCMetric(data.read_psd(args.psd_xml_gz, "H1", verbose=True),
					  cf(**bounds),
					  flow=args.flow, fhigh=args.fhigh,
					  approximant="IMRPhenomD")

	compute_bank_size(g,
					  args.min_m1, args.max_m1, args.m1_size,
					  args.min_m2, args.max_m2, args.m2_size,
					  args.min_chi, args.max_chi, args.chi_size,
					  args.spin, args.method, args.mm)


if __name__ == '__main__':
	main()
