import bisect
import pathlib
import sys
from typing import Union

import lal
import lalsimulation as lalsim
import numpy
from ligo.lw import ligolw
from ligo.lw import lsctables
from ligo.lw import utils
from ligo.lw.utils import process as ligolw_process
from numpy import log10 as l10
from scipy.special import erf, logsumexp
from scipy.interpolate import splrep, PPoly


from manifold import metric, signal, cover, coordinate
from manifold.utilities import data, common


# Define CBC Coordinate Types

class M1(coordinate.CoordinateType):
	"""Mass 1"""
	key = 'm1'


class M2(coordinate.CoordinateType):
	"""Mass 2"""
	key = 'm2'


class LogM1(coordinate.CoordinateType):
	"""Log10 Mass 1"""
	key = 'log10m1'


class LogM2(coordinate.CoordinateType):
	"""Log10 Mass 2"""
	key = 'log10m2'


class S1X(coordinate.CoordinateType):
	"""Spin 1 x-component"""
	key = 'S1x'


class S1Y(coordinate.CoordinateType):
	"""Spin 1 y-component"""
	key = 'S1y'


class S1Z(coordinate.CoordinateType):
	"""Spin 1 z-component"""
	key = 'S1z'


class S2X(coordinate.CoordinateType):
	"""Spin 2 x-component"""
	key = 'S2x'


class S2Y(coordinate.CoordinateType):
	"""Spin 2 y-component"""
	key = 'S2y'


class S2Z(coordinate.CoordinateType):
	"""Spin 2 z-component"""
	key = 'S2z'


class Chi(coordinate.CoordinateType):
	key = 'chi'


class MC(coordinate.CoordinateType):
	key = 'mc'


#
# Utility functions to help with the coordinate system for evaluating the waveform metric
#

def expand(x):
	# map [-1,1] -> [-inf, inf]
	return numpy.tan(x * numpy.pi / 2)


def crush(x):
	# map [-inf,inf] -> [-1, 1]
	return (numpy.arctan(x) * 2 / numpy.pi)


def chirpmass(m1, m2):
	return (m1 * m2) ** .6 / (m1 + m2) ** .2


def mi_from_mc_mj(mc, m2):
	p = -mc ** 5 / m2 ** 3
	q = -mc ** 5 / m2 ** 2

	def t(k, p, q):
		return 2 * (-p / 3.) ** .5 * numpy.cos(1. / 3. * numpy.arccos(3 * q / (2 * p) * (-3. / p) ** .5) - 2 * numpy.pi * k / 3.)

	def t3(p, q):
		return -2 * numpy.abs(q) / q * (-p / 3.) ** .5 * numpy.cosh(1. / 3. * numpy.arccosh(-3. * abs(q) / 2. / p * (-3. / p) ** .5))

	out = numpy.array([[t(i, p, q) for i in range(3)] + [t3(p, q)]])
	try:
		return numpy.nanmax(out, axis=1)
	except numpy.core._internal.AxisError:
		return numpy.nanmax(out)


def z_from_m1_m2_s1_s2(m1, m2, s1, s2):
	m1 = float(m1)
	m2 = float(m2)
	s1 = float(s1)
	s2 = float(s2)
	M = m1 + m2
	return (s1 * m1 + s2 * m2) / M


def zn_from_m1_m2_s1_s2(m1, m2, s1, s2):
	m1 = float(m1)
	m2 = float(m2)
	s1 = float(s1)
	s2 = float(s2)
	M = m1 + m2
	return (s1 * m1 - s2 * m2) / M


def s1_from_m1_m2_z_zn(m1, m2, z, zn):
	M = m1 + m2
	return (z + zn) * M / m1 / 2.


def s2_from_m1_m2_z_zn(m1, m2, z, zn):
	M = m1 + m2
	return (z - zn) * M / m2 / 2.


CBC_COORD_TRANSFORMS = {
	# Mapping of (from types), (to types): transform function
	((M1,), (LogM1,)): l10,
	((M2,), (LogM2,)): l10,
	((LogM1,), (M1,)): lambda x: 10 ** x,
	((LogM2,), (M2,)): lambda x: 10 ** x,
	((M1, M2), (MC,)): chirpmass,
	((M1, M2, S1Z, S2Z), (Chi,)): z_from_m1_m2_s1_s2,
}


class CBCCoordFunc(coordinate.CoordFunc):
	_STANDARD_COORD_TYPES = (M1, M2, S1X, S1Y, S1Z, S2X, S2Y, S2Z,)

	def dx(self, c: coordinate.Coordinates):
		return metric.DELTA * numpy.ones(len(c))

	def random(self):
		# TODO find a smarter way to draw uniformly over chi
		# might be a bad idea if people have very different priors for the two components
		if S1Z in self.to_bounds:
			s = numpy.random.uniform(min(self.to_bounds[S1Z][0], self.to_bounds[S2Z][0]), max(
				self.to_bounds[S1Z][1], self.to_bounds[S2Z][1]))
		else:
			s = 0
		m1 = 10 ** numpy.random.uniform(numpy.log10(self.to_bounds[M1][0]), numpy.log10(self.to_bounds[M1][1]))
		m2 = 10 ** numpy.random.uniform(numpy.log10(self.to_bounds[M2][0]), numpy.log10(m1))
		rp = {M1: m1,
			  M2: m2,
			  S1Z: s,
			  S2Z: s,
			  S1X: 0.,
			  S1Y: 0.,
			  S2X: 0.,
			  S2Y: 0.}
		if rp[M1] < rp[M2]:
			m1, s1x, s1y, s1z = rp[M1], rp[S1X], rp[S1Y], rp[S1Z]
			rp[M1], rp[S1X], rp[S1Y], rp[S1Z] = rp[M2], rp[S2X], rp[S2Y], rp[S2Z]
			rp[M2], rp[S2X], rp[S2Y], rp[S2Z] = m1, s1x, s1y, s1z
		return rp

	@property
	def base_step(self):
		return .01


class Log10M1Log10M2(CBCCoordFunc):
	key = "log10m1_log10m2"

	TO_TYPES = (M1, M2)
	FROM_TYPES = (LogM1, LogM2)

	def __call__(self, c: Union[coordinate.Coordinates, coordinate.CoordsDict], inv: bool = False):
		if inv:
			c = self._normalize_coorddict(c, inv=True)
			m1, m2 = c[M1], c[M2]
			return numpy.array([l10(m1), l10(m2)])
		else:
			m1 = 10 ** c[..., 0]
			m2 = 10 ** c[..., 1]
			try:
				return {M1: float(m1), M2: float(m2)}
			except (ValueError, TypeError):  # must be array
				return [{M1: a, M2: b} for (a, b) in numpy.array([m1, m2]).T]

	@property
	def min_eig_val(self):
		return 0.0  # 25

	def base_step(self, coords):
		return .01

	def target_match(self, c):
		return 1. - 0.7 * numpy.finfo(numpy.float32).eps


class Log10M1Log10M2Chi(CBCCoordFunc):
	key = "log10m1_log10m2_chi"

	TO_TYPES = (M1, M2, S1Z, S2Z)
	FROM_TYPES = (LogM1, LogM2, Chi)

	def __call__(self, c: Union[coordinate.Coordinates, coordinate.CoordsDict], inv=False):
		if inv:
			c = self._normalize_coorddict(c, inv=True)
			m1, m2, s1, s2 = c[M1], c[M2], c[S1Z], c[S2Z]
			chi = z_from_m1_m2_s1_s2(m1, m2, s1, s2)
			return numpy.array([l10(m1), l10(m2), chi])
		else:
			m1 = 10 ** c[..., 0]
			m2 = 10 ** c[..., 1]
			s1z = c[..., 2]
			s2z = c[..., 2]
			try:
				return {M1: float(m1), M2: float(m2), S1Z: float(s1z), S2Z: float(s2z)}
			except (ValueError, TypeError):  # must be array
				return [{M1: a, M2: b, S1Z: c, S2Z: d} for (a, b, c, d) in numpy.array([m1, m2, s1z, s2z]).T]

	@property
	def min_eig_val(self):
		return 0.0  # 25

	def base_step(self, coords):
		return .01

	def target_match(self, c):
		return 1 - 0.7 * numpy.finfo(numpy.float32).eps

	def salpeter_prob(self, r):
		c = self(r.center)
		m1 = c[M1]
		m2 = c[M2]
		chi = (c[M1] * c[S1Z] + c[M2] * c[S2Z]) / (c[M1] + c[M2])
		# Assumes uniform in chi and m2
		volume = 10**r.size[0] * 10**r.size[1] * r.size[2]
		return (m1, m2, chi), m1**-(2.35) * volume

#
# Metric object that numerically evaluates the waveform metric


class CBCMetric(metric.Metric):
	"""
    Class to numerically evaluate the compact binary parameter space metric.

    Parameters
    ----------
    psd: REAL8FrequencySeries
        A LAL type holding a PSD
    coord_func: coord_func
        A coord_func or derived class that specifies the coordinate transformation.
    duration: int, default4
        The duration of waveform to produce 
    flow: float, default=15.
        The minimum frequency of the integration
    fhigh: float, default=512
        The maximum frequency of the integration
    approximant: str, default="IMRPhenomD"
        Currently only TaylorF2 and IMRPhenomD are supported

    Examples
    --------
    >>> psd = io.h5read('test_data/H1L1-MASS_BBH-1185149070-800.h5', 'psd')['L1']
    >>> bounds = {"m1":[1., 100.], "m2":[1., 100.], "S1z":[-1., 1.], "S2z":[-1., 1.]}
    >>> cfunc = metric.m1_m2_s1z_s2z(bounds)
    >>> g = metric.CBCMetric(psd, cfunc)
    >>> g([1.4, 1.4, 0, 0])
    array([[ 4.34726584e+05,  4.34725714e+05, -8.52915457e+03,
            -8.52915457e+03],
           [ 4.34725714e+05,  4.34726584e+05, -8.52915457e+03,
            -8.52915457e+03],
           [-8.52915457e+03, -8.52915457e+03,  1.82025977e+02,
             1.81156190e+02],
           [-8.52915457e+03, -8.52915457e+03,  1.81156190e+02,
             1.82025977e+02]])
    """
	WAVEFORM_COORDS = (M1, M2, S1X, S1Y, S1Z, S2X, S2Y, S2Z)
	WAVEFORM_COORD_DEFAULTS = {S1X: 0., S1Y: 0., S1Z: 0., S2X: 0., S2Y: 0., S2Z: 0.}

	def __init__(self, psd=None, coord_func=None, flow=15.0, fhigh=512., approximant="IMRPhenomD", max_metric_diff: float = metric.DEFAULT_MAX_DIFF_THRESHOLD, max_duration: float = numpy.inf):
		self.appxstr = approximant
		self.approximant = lalsim.GetApproximantFromString(approximant)
		self.max_duration = max_duration
		metric.Metric.__init__(self, psd, coord_func, flow, fhigh, max_metric_diff=max_metric_diff)

	def _to_dict(self):
		return {"psd": self.psd, "coord_func": {self.coord_func.key: self.coord_func.to_dict()}, "flow": self.freq_low, "fhigh": self.freq_high, "approximant": self.appxstr, "max_metric_diff": self.max_diff_threshold, "max_duration": self.max_duration}

	@classmethod
	def _from_dict(cls, d):
		# FIXME this is silly - fix how we encode these objects generally and especially the coord functions
		k, v = tuple(d['coord_func'].items())[0]
		d['coord_func'] = coord_funcs[k](**v)

		return cls(**d)

	def waveform(self, c: coordinate.Coordinates):

		# FIXME replace with something more accurate
		def f_at_t(mc, t):
			M = mc * 4.93e-6 # convert solar mass to seconds
			return 1 / numpy.pi / M * (5./256 * M / t)**(3./8)

		# Generalize to different waveform coords
		parameters = self.coord_func(c)

		# FIXME this could be a bad idea since we are taking derivatives. 
		parameters[S1Z] = min(max(parameters[S1Z], -0.999), 0.999)
		parameters[S2Z] = min(max(parameters[S2Z], -0.999), 0.999)


		# Figure out if we need to adjust the low frequency to limit waveform duration
		if numpy.isfinite(self.max_duration):
			flow = max(f_at_t(chirpmass(parameters[M1], parameters[M2]), self.max_duration), self.freq_low)
		else:
			flow = self.freq_low

		try:
			parameters[M1] *= lal.MSUN_SI
			parameters[M2] *= lal.MSUN_SI

			parameters['distance'] = 1.e6 * lal.PC_SI
			parameters['inclination'] = 0.
			parameters['phiRef'] = 0.
			parameters['longAscNodes'] = 0.
			parameters['eccentricity'] = 0.
			parameters['meanPerAno'] = 0.
			parameters['deltaF'] = self.freq_interval
			parameters['f_min'] = flow
			parameters['f_max'] = self.freq_high
			parameters['f_ref'] = 0.
			parameters['LALparams'] = None
			parameters['approximant'] = self.approximant

			parameters = self._normalize_waveform_params(parameters)

			hplus, hcross = lalsim.SimInspiralFD(**parameters)

			fseries = hplus
			lal.WhitenCOMPLEX16FrequencySeries(fseries, self.psd)
			fseries = signal.add_quadrature_phase(fseries, self.working_length)

			# TODO why the manual del, is there some lalsim side effect we need to clear?
			del hplus
			del hcross
		except RuntimeError as p:
			# TODO fix this reference / switch to logging
			print(p)
			# raise
			return None
		return fseries


#
# register coord funcs
#

coord_funcs = {
	# Tested coord funcs
	Log10M1Log10M2.key: Log10M1Log10M2,
	Log10M1Log10M2Chi.key: Log10M1Log10M2Chi,
}


#
# Bank specific classes
#

class ManifoldRectangle(cover.ManifoldRectangle):
	@property
	def metric_center(self):
		# FIXME for now this just returns the actual center of the rectangle
		return self.center

	def match(self, other):
		if type(other) == type(self):
			return self.metric.metric_match(self.g, self.center, other.center)
		elif type(other) == numpy.ndarray:
			return self.metric.metric_match(self.g, self.center, other)
		else:
			raise ValueError("argument %s not supported" % type(other))

	def fft_match(self, others):
		w1 = self.metric.waveform(self.center)
		return numpy.array([self.metric.fft_match(w1, self.metric.waveform(other.center)) for other in others])

	@property
	def sngl_row(self):
		# FIXME also include other relevant paramters here that are known e.g., flow, approximant, instrument, etc.
		d = self.metric._normalize_waveform_params(self.metric.coord_func(self.center))
		rdict = {k:0 for k in ("process:process_id", "ifo", "search", "channel", "end_time", "end_time_ns", "end_time_gmst", "impulse_time", "impulse_time_ns", "template_duration", "event_duration", "amplitude", "eff_distance", "coa_phase", "mass1", "mass2", "mchirp", "mtotal", "eta", "kappa", "chi", "tau0", "tau2", "tau3", "tau4", "tau5", "ttotal", "psi0", "psi3", "alpha", "alpha1", "alpha2", "alpha3", "alpha4", "alpha5", "alpha6", "beta", "f_final", "snr", "chisq", "chisq_dof", "bank_chisq", "bank_chisq_dof", "cont_chisq", "cont_chisq_dof", "sigmasq", "rsqveto_duration", "Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7", "Gamma8", "Gamma9", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "event_id")}
		rdict.update({"ifo":"L1", "process_id":0, "mass1":d['m1'], "mass2":d['m2'], "spin1x":d['S1x'], "spin1y":d['S1y'], "spin1z":d['S1z'], "spin2x":d['S2x'], "spin2y":d['S2y'], "spin2z":d['S2z']})
		return lsctables.SnglInspiralTable.RowType(**rdict)


class Chart(cover.Chart):
	pass

def _pn_phase(d):
	# From https://arxiv.org/pdf/1107.1267.pdf
	m1, m2, s1, s2 = d[M1] * 5e-6, d[M2] * 5e-6, d[S1Z], d[S2Z] # mass in seconds
	mc = (m1*m2)**.6 / (m1+m2)**.2
	return mc
#	m = m1 + m2
#	eta = m1 * m2 / m**2
#	chi = (m1*s1 + m2*s2) / m
#	delta = (m1 - m2) / 2
#	xs = (s1 + s2) / 2.
#	xa = (s1 - s2) / 2.
#	beta = 113 / 12. * (xs + delta * xa - 76 * eta / 113. * xs)
#	sigma = xa**2 * (81/16. - 20 * eta) + 81 * xa * xs / 8. + xs**2 * (81/16. - eta / 4.)
#	gamma = xa * delta * (140 * eta / 9. + 732985 / 2268.) + xs * ( 732985 / 2268. - 24260. * eta / 81 - 340. * eta**2 / 9)
#	def phase(f, m = m, eta = eta, beta = beta, sigma = sigma):
#		v = (numpy.pi * m * f)**(1./3.)
#		return 3. / (128 * eta) * (
#			v**-5 +
#			v**-3 * (55 * eta / 9. +
#				3715/756.) +
#			v**-2 * (4 * beta -
#				16 * numpy.pi) +
#			v**-1 * (3085 * eta**2 / 72. +
#				27145 * eta / 504 +
#				15293365 / 508032 - 10 * sigma) +
#			v**0 * (38645*numpy.pi / 756 -
#				65 * numpy.pi * eta / 9 -
#				gamma) * (3 * numpy.log(v) + 1) + 
#			v**1 * (-6848 / 21. * numpy.euler_gamma -
#				127825 * eta**3 / 1296 +
#				76055 * eta**2 / 1728. +
#				(2255 * numpy.pi**2 / 12 - 15737765635 / 3048192.) -
#				640 * numpy.pi**2 / 3 +
#				11583231236531 / 4694215680. -
#				6848 * numpy.log(4 * v) / 21. ) +
#			v**2 * (-74045 * numpy.pi * eta**2 / 756. +
#				378515 * numpy.pi * eta / 1512. +
#				77096675 * numpy.pi / 254016)
#			)
#	# 1 looks pretty good
#	return phase(1024) - phase(1)


class Bank(object):
	def __init__(self, rectangles, constraints = {}, ids = None):
		self.rectangles = rectangles
		self.constraints = constraints
		self.cfunc = self.rectangles[0].metric.coord_func
		self.sorted = False
		if ids is None:
			self.assign_ids()
		else:
			self.ids = ids

	def __len__(self):
		return len(self.rectangles)

	def assign_ids(self):
			self.ids = numpy.arange(len(self.rectangles))

	def sort(self):
		rs = sorted([(_pn_phase(r.metric.coord_func(r.center)), n, r) for n,r in zip(self.ids, self.rectangles)])
		self.pns = [r[0] for r in rs]
		self.rectangles = [r[-1] for r in rs]
		self.centers = numpy.array([r.center for r in self.rectangles])
		self.ids = numpy.array([r[1] for r in rs])
		self.sorted = True

	def split(self):
		left = [r for r in self.rectangles if r.left]
		idsleft = [ID for ID, r in zip(self.ids, self.rectangles) if r.left]
		right = [r for r in self.rectangles if r.right]
		idsright = [ID for ID, r in zip(self.ids, self.rectangles) if r.right]
		return Bank(left, self.constraints, ids = idsleft), Bank(right, self.constraints, ids = idsright)

	def group(self, num):
		# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
		def __split(a, n):
			k, m = divmod(len(a), n)
			return ( (i*k+min(i, m), (i+1)*k+min(i+1, m)) for i in range(n))
			#return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
		for (six, eix) in __split(self.rectangles, num):
			yield Bank(self.rectangles[six:eix], self.constraints, ids=self.ids[six:eix])

	def inside(self, r, check_vertices = True):
		out = True
		for func in [Bank.m1_constraint, Bank.m2_constraint, Bank.M_constraint, Bank.mc_constraint, Bank.q_constraint, Bank.chi_constraint]:
			if check_vertices:
				points = list(r.vertices) + [list(r.center)]
			else:
				points = [list(r.center)]
			out &= not all(func(self.constraints, self.cfunc(numpy.array(v))) for v in points)
		return out

	def trim(self, verbose = True):
		if verbose: print ("%d templates before" % len(self.rectangles))
		data = [(r,ID) for r,ID in zip(self.rectangles, self.ids) if self.inside(r)]
		self.rectangles = [x[0] for x in data]
		self.ids = [x[1] for x in data]
		if verbose: print ("%d templates after" % len(self.rectangles))

	def hardcut(self, verbose = True):
		if verbose: print ("%d templates before" % len(self.rectangles))
		data = [(r,ID) for r,ID in zip(self.rectangles, self.ids) if self.inside(r, check_vertices = False)]
		self.rectangles = [x[0] for x in data]
		self.ids = [x[1] for x in data]
		if verbose: print ("%d templates after" % len(self.rectangles))

	def neighborhood_overlaps(self, ix, n = 100000):
		if not self.sorted:
			raise ValueError("indexing into this bank without calling sort() first will lead to nonsense. This is probably wrong")
		if ix < n / 2:
			ixL = 0
		else:
			ixL = ix - n // 2
		ixR = ixL + n
		if ixR > len(self.rectangles):
			ixR = len(self.rectangles)
		return self.rectangles[ix].match(self.centers[ixL:ixR]), numpy.arange(ixL, ixR)

	def nearest(self, c, n = 30000):
		if not self.sorted:
			self.sort()
		pn = _pn_phase(c)
		ix = bisect.bisect(self.pns, pn)
		if ix < n / 2:
			ixL = 0
		else:
			ixL = ix - n // 2
		ixR = ixL + n
		this_rs = self.rectangles[ixL:ixR]

		cp = self.cfunc(c, inv=True)

		def _fft_match(x, cp = cp):
			return x[-1].metric.fft_match_at_coords(cp, x[-1].center)
		return max(map(_fft_match, enumerate(this_rs)))

	def prob_of_tk_given_rho(self, p_of_tj_given_alpha, num_rhos = 50, n = 50000, verbose = True):

		rhos = numpy.logspace(0.5, 2, num_rhos)
		log_p_of_tk_given_alpha_rho = numpy.zeros((len(rhos), len(p_of_tj_given_alpha)))
		rootpiby2 = numpy.sqrt(numpy.pi/2.0)
            
		for ix in range(len(self)):
			kdj, indices = self.neighborhood_overlaps(ix, n = n)
			log_p_of_tj_given_alpha = numpy.nan_to_num(numpy.log( p_of_tj_given_alpha[indices] +1.0e-310))
			kdj4 = kdj**4
			kdj3 = kdj**3
			kdj2 = kdj**2
			for jx, rho in enumerate(rhos):
				# factor out norm of e^(rho^/2)
				log_p_of_tk_given_alpha_rho[jx,ix] = logsumexp(log_p_of_tj_given_alpha+0.5*(rho**2)*kdj2+numpy.log(rootpiby2*erf(rho*kdj/ 2**.5) * ((rho**4)*kdj4 + 6 * (rho**2)*kdj2 + 3.) + numpy.exp(-0.5*(rho**2)*kdj2)*((rho**3)*kdj3 + 5 *rho*kdj)))
				if numpy.isnan(log_p_of_tk_given_alpha_rho[jx,ix]):
					raise ValueError("%d has nan overlaps" % ix)
			if verbose and not ix % 100:
				print ("processing row %d" % (ix,))

		# normalize the result
		for jx, rho in enumerate(rhos):
			log_p_of_tk_given_alpha_rho[jx,:] -= logsumexp(log_p_of_tk_given_alpha_rho[jx,:])
		#and create the piecewise polynomial fit TO THE NATURAL LOG
		coefficients = numpy.zeros((4, num_rhos + 3, len(p_of_tj_given_alpha)), dtype=float)
		breakpoints = numpy.zeros(num_rhos + 4, dtype=float)
		for tix in range(log_p_of_tk_given_alpha_rho.shape[1]):
			tck = splrep(rhos,log_p_of_tk_given_alpha_rho[:,tix])
			p = PPoly.from_spline(tck)
			coefficients[:,:,tix] = p.c
			if tix==0:
				breakpoints[:] = p.x

		return coefficients, breakpoints

	@staticmethod
	def m1_constraint(constraints, c):
		return (c[M1] < constraints['m1'][0]) or (c[M1] > constraints['m1'][1])

	@staticmethod
	def m2_constraint(constraints, c):
		return (c[M2] < constraints['m2'][0]) or (c[M2] > constraints['m2'][1])

	@staticmethod
	def M_constraint(constraints, c):
		M = c[M1] + c[M2]
		return (M < constraints['M'][0]) or (M > constraints['M'][1])

	@staticmethod
	def mc_constraint(constraints, c):
		mc = chirpmass(c[M1], c[M2])
		return (mc < constraints['mc'][0]) or (mc > constraints['mc'][1])

	@staticmethod
	def q_constraint(constraints, c):
		q = c[M1] / c[M2]
		return (q < constraints['q'][0]) or (q > constraints['q'][1])

	@staticmethod
	def chi_constraint(constraints, c):
		m1, m2 = c[M1], c[M2]
		chi = (c[M1] * c[S1Z] + c[M2] * c[S2Z]) / (c[M1] + c[M2])
		min_chi, max_chi = constraints['chi']
		min_ns_mass, max_ns_mass = constraints['ns-mass']
		min_ns_s1z, max_ns_s1z = constraints['ns-s1z']
		# if both m1 and m2 are NS, then chi must be the same interval as the ns spin
		if (min_ns_mass <= m1 <= max_ns_mass) and (min_ns_mass <= m2 <= max_ns_mass):
			return (chi < min_ns_s1z) or (chi > max_ns_s1z)
		# m1 is an NS
		if (min_ns_mass <= m1 <= max_ns_mass) and  not (min_ns_mass <= m2 <= max_ns_mass):
			min_chi = max(min_chi, (min_ns_s1z * m1 - m2) / (m1 + m2))
			max_chi = min(max_chi, (max_ns_s1z * m1 + m2) / (m1 + m2))
			return (chi < min_chi) or (chi > max_chi)
		# m2 is an NS
		if not (min_ns_mass <= m1 <= max_ns_mass) and  (min_ns_mass <= m2 <= max_ns_mass):
			min_chi = max(min_chi, (-m1 + min_ns_s1z * m2) / (m1 + m2))
			max_chi = min(max_chi, (m1 + max_ns_s1z * m2) / (m1 + m2))
			return (chi < min_chi) or (chi > max_chi)
		# neither m1 nor m2 are NS
		if chi < constraints['chi'][0] or chi > constraints['chi'][1]:
			return True
		return False

	def constraint(self, c):
		return any(f(self.constraints, c) for f in [Bank.m1_constraint, Bank.m2_constraint, Bank.M_constraint, Bank.mc_constraint, Bank.q_constraint, Bank.chi_constraint])

	def split_cell(self, ix):
		l,r = self.rectangles[ix].divide()
		self.rectangles.pop(ix)
		self.mcs.pop(ix)

		for c in (l, r):
			d = self.cfunc(c.center)
			mc = chirpmass(d[M1], d[M2])
			ix = bisect.bisect(self.mcs, mc)
			self.mcs.insert(ix, mc)
			self.rectangles.insert(ix, c)
			self.ids.insert(ix, max(self.ids)+1)

	def refine(self, mm, n = 20000, m = 20, to_check = None, verbose = False):
		self.sort()
		new_rectangles = []
		added = 0

		best_matches_rectangles = {}
		removed_rectangles = set()
		added_rectangles = set()
		dim = len(self.rectangles[0].center)
		for ix, r in enumerate(self.rectangles):
			if verbose and not ix % 1000: print("processing template %d, added %d so far" % (ix, added))
			if to_check is not None and r not in to_check:
				new_rectangles.append(r)
				continue
			matches, ixs = self.neighborhood_overlaps(ix, n=n)
			# verify with FFT matches if requested
			if m:
				local_ixs = numpy.argsort(matches)[-m:]
				local_matches = r.fft_match([self.rectangles[ixs[local_ix]] for local_ix in local_ixs])
				for _n, local_ix in enumerate(local_ixs):
					matches[local_ix] = local_matches[_n]
			# find the best match "on the diagonal" ignore the best match which is with itself.
			best_match_local_ix = numpy.argsort(matches)[-2]
			best_match_global_ix = ixs[best_match_local_ix]
			match = matches[best_match_local_ix]
			best_matches_rectangles.setdefault(self.rectangles[best_match_global_ix], set()).add(r)
			if 1-match > 2 * mm:
				right, left = r.divide(reuse_g = True)
				inright = self.inside(right)
				inleft = self.inside(left)
				if inright:
					new_rectangles.append(right)
					added_rectangles.add(right)
					added += 1
				if inleft:
					new_rectangles.append(left)
					added_rectangles.add(left)
					added += 1
				if (not inright) and (not inleft):
					new_rectangles.append(r)
				else:
					added -=1
					removed_rectangles.add(r)
			else:
				new_rectangles.append(r)

		if verbose: print("calculating which templates have changed")
		to_check = set()
		for r in removed_rectangles:
			if r in best_matches_rectangles and r not in removed_rectangles:
				for r2 in best_matches_rectangles[r]:
					to_check.add(r2)
		to_check |= added_rectangles

		assert not to_check - set(new_rectangles)
		if verbose: print("Done")

		return Bank(new_rectangles, constraints = self.constraints), to_check


	@classmethod
	def fromChart(cls, chart, constraints={}):
		return cls(tuple(chart.atlas()), constraints=constraints)

	@classmethod
	def load(cls, h5fn):
		# @shio figure out how to parse the file back in and make one of these Bank classes
		d = data.read_h5(h5fn)
		metric = CBCMetric._from_dict(d['metric'])
		rectangles = []
		for mn, mx, g, right, left, in zip(d['mins'], d['maxes'], d['gs'], d['rights'], d['lefts']):
			rectangles.append(ManifoldRectangle(mn, mx, metric, g, right=right, left=left))
		return cls(rectangles, constraints = d['constraints'], ids = None if 'ids' not in d else d['ids'])

	def save(self, h5fn):
		# FIXME @shio please find a way to serialize the data in a metric so that it can be recorded to hdf5
		# FIXME completely untested

		out = {	"metric": self.rectangles[0].metric._to_dict(),
			"mins": numpy.array([r.mins for r in self.rectangles]),
			"maxes": numpy.array([r.maxes for r in self.rectangles]),
			"gs": numpy.array([r.g for r in self.rectangles]),
			"rights": numpy.array([r.right for r in self.rectangles]),
			"lefts": numpy.array([r.left for r in self.rectangles]),
			"constraints": self.constraints,
			"ids": self.ids,
		      }
		io.h5write(h5fn, out)

	def to_ligolw(self, xmlfn, program_name = None, optdict = {}):
		# prepare a new XML document for writing template bank
		xmldoc = ligolw.Document()
		xmldoc.appendChild(ligolw.LIGO_LW())
		sngl_inspiral_columns = ("process:process_id", "ifo", "search", "channel", "end_time", "end_time_ns", "end_time_gmst", "impulse_time", "impulse_time_ns", "template_duration", "event_duration", "amplitude", "eff_distance", "coa_phase", "mass1", "mass2", "mchirp", "mtotal", "eta", "kappa", "chi", "tau0", "tau2", "tau3", "tau4", "tau5", "ttotal", "psi0", "psi3", "alpha", "alpha1", "alpha2", "alpha3", "alpha4", "alpha5", "alpha6", "beta", "f_final", "snr", "chisq", "chisq_dof", "bank_chisq", "bank_chisq_dof", "cont_chisq", "cont_chisq_dof", "sigmasq", "rsqveto_duration", "Gamma0", "Gamma1", "Gamma2", "Gamma3", "Gamma4", "Gamma5", "Gamma6", "Gamma7", "Gamma8", "Gamma9", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "event_id")
		tbl = lsctables.New(lsctables.SnglInspiralTable, columns = sngl_inspiral_columns)
		xmldoc.childNodes[-1].appendChild(tbl)
		# FIXME make a real process table
		process = ligolw_process.register_to_xmldoc(xmldoc, program_name or sys.argv[0], optdict)
		process.set_end_time_now()


		for n, c in zip(self.ids, self.rectangles):
			center_dict = self.cfunc(numpy.array(c.center))
			row = c.sngl_row
			row.f_final = 1024#FIXME!!!
			row.mchirp = chirpmass(center_dict[M1], center_dict[M2])
			row.process_id = process.process_id
			row.event_id = n
			row.template_id = n
			tbl.append(row)

		# Write out the bank file
		utils.write_filename(xmldoc, xmlfn)


# FIXME are these functions below used??

def metric_m1_m2(min_mass, max_mass, psd_path: pathlib.Path = data.TREEBANK_PSD, detector: str = 'H1', verbose: bool = False,
				 freq_low: int = 15, freq_high: int = 512):
	g = CBCMetric(data.read_psd(psd_path, detector, verbose=verbose),
				  M1M2(**common.bounds_from_lists(['m1', 'm2'], [min_mass, min_mass], [max_mass, max_mass])),
				  freq_low, freq_high, approximant="IMRPhenomD")
	return g


def bank_m1_m2(min_mass, max_mass, psd_path: pathlib.Path = data.TREEBANK_PSD, detector: str = 'H1', verbose: bool = False,
			   freq_low: int = 15, freq_high: int = 512, reuse_g_mm: float = 0.0):
	g = metric_m1_m2(min_mass, max_mass, psd_path, detector, verbose, freq_low, freq_high)
	R = ManifoldRectangle(g.coord_func.mins, g.coord_func.maxes, g)
	Bank = cover.Chart(R)

	# FIXME this constraint function only makes sense if the first two coordinates are m1, m2
	def constraint(o):
		return not all(v[0] < v[1] for v in o.data.vertices)

	Bank.branch(mm=10.0,
				reuse_g_mm=reuse_g_mm,
				constraint=constraint,
				verbose=False)

	return Bank
