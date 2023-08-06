"""Metric

References:
	[1] B. J. Owen, Search Templates for Gravitational Waves from Inspiraling Binaries: Choice of Template Spacing, Phys. Rev. D 53, 6749 (1996).
"""

import itertools
import types

import lal
import numpy
from scipy import optimize

from manifold import signal, coordinate
from manifold.utilities import common

DEFAULT_F_LOW = 10.0
DEFAULT_F_HIGH = 1024.0
DEFAULT_DURATION = 1
MAX_EPSILON_SCALE = 2 * numpy.finfo(numpy.float32).eps
DEFAULT_TARGET_MATCH = 1. - .5 * numpy.finfo(numpy.float32).eps
DEFAULT_MAX_DIFF_THRESHOLD = 0.7
MIN_TARGET_MATCH = 0.90

def _getAplus(A):
    eigval, eigvec = numpy.linalg.eig(A)
    Q = numpy.matrix(eigvec)
    xdiag = numpy.matrix(numpy.diag(numpy.maximum(eigval, 0)))
    return Q*xdiag*Q.T

def _getPs(A, W=None):
    W05 = numpy.matrix(W**.5)
    return  W05.I * _getAplus(W05 * A * W05) * W05.I

def _getPu(A, W=None):
    Aret = numpy.array(A.copy())
    Aret[W > 0] = numpy.array(W)[W > 0]
    return numpy.matrix(Aret)

def nearPD(A, nit=10):
    n = A.shape[0]
    W = numpy.identity(n) 
# W is the matrix used for the norm (assumed to be Identity matrix here)
# the algorithm should work for any diagonal W
    deltaS = 0
    Yk = A.copy()
    for k in range(nit):
        Rk = Yk - deltaS
        Xk = _getPs(Rk, W=W)
        deltaS = Xk - Rk
        Yk = _getPu(Xk, W=W)
    return Yk


class EvaluationMethod:
	"""Enum of evaluation methods"""
	Numeric = 'numeric'
	Deterministic = 'deterministic'


# Gaussian = 'gaussian' # TODO uncomment when completed


class EvaluationError(ValueError):
	pass


class EigenvalueError(EvaluationError):
	pass


class MaxDiffError(EvaluationError):
	pass


class Metric(object):
	"""Class to numerically evaluate a waveform parameter space metric.

	Examples:
		>>> psd = data.read_h5('tests/data/H1L1-MASS_BBH-1185149070-800.h5', 'psd')['L1']
		>>> bounds = {"m1":[1., 100.], "m2":[1., 100.], "S1z":[-1., 1.], "S2z":[-1., 1.]}
		>>> cfunc = m1_m2_s1z_s2z(bounds)
		>>> g = Metric(psd, cfunc)
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
	WAVEFORM_COORDS = ()  # overridden by subclasses
	WAVEFORM_COORD_DEFAULTS = {}  # overridden by subclasses

	def __init__(self, psd, coord_func: types.FunctionType, f_low: float = DEFAULT_F_LOW, f_high: float = DEFAULT_F_HIGH, duration: int = DEFAULT_DURATION,
				 max_metric_diff: float = DEFAULT_MAX_DIFF_THRESHOLD):
		"""Create a Metric

		Args:
			psd:
				REAL8FrequencySeries, A LAL type holding a PSD
			coord_func:
				Fucntion, a coord_func or derived class that specifies the coordinate transformation.
			f_low:
				float, default=15, the minimum frequency of the integration
			f_high:
				float, default=512, the maximum frequency of the integration
			duration:
				int, default 4, the time step that determines the frequency interval as freq_interval = 1/duration
		Returns:
			Metric
		"""
		# TODO we should investigate how the duration affects this
		self.duration = duration
		self.coord_func = coord_func
		self.freq_interval = 1. / self.duration
		self.freq_low = f_low
		self.freq_high = f_high
		self.working_length = int(round(self.duration * 2 * self.freq_high)) + 1
		self.psd = signal.interpolate_psd(psd, self.freq_interval)
		self.revplan = lal.CreateReverseCOMPLEX16FFTPlan(self.working_length, 1)
		self.freq_vec = numpy.arange(self.working_length) * self.freq_interval
		self.t_series = lal.CreateCOMPLEX16TimeSeries(
			name="workspace",
			epoch=0,
			f0=0,
			deltaT=1. / (2 * self.freq_high),
			length=self.working_length,
			sampleUnits=lal.Unit("strain")
		)
		self.f_series = lal.CreateCOMPLEX16FrequencySeries(
			name="template",
			epoch=0.0,
			f0=0.0,
			deltaF=self.freq_interval,
			sampleUnits=lal.Unit("strain"),
			length=self.working_length
		)
		self._method_funcs = {
			EvaluationMethod.Numeric: self._evaluate_hessian,
			EvaluationMethod.Deterministic: self._evaluate_deterministic,
		}
		self.max_diff_threshold = max_metric_diff

	def __call__(self, center: coordinate.Coordinates, scale=None):
		"""Syntactic sugar wrapper around evaluate method"""
		return self.evaluate(center, scale=scale)

	def _normalize_waveform_params(self, d: coordinate.CoordsDict):
		n = d.copy()

		# Set defaults
		for k, v in self.WAVEFORM_COORD_DEFAULTS.items():
			if k not in n:
				n[k] = v

		# Replace types with keys (so can be unpacked into waveform func)
		for t in self.WAVEFORM_COORDS:
			if t in n:
				n[t.key] = n.pop(t)

		return n

	def _distancesq(self, metric_tensor, x, y) -> float:

		delta = x - y
		X = numpy.dot(delta, metric_tensor)
		Y = delta
		d2 = numpy.sum((X * Y), axis=1)
		d2[d2 < 0.] = 0.
		return d2

	def distance(self, metric_tensor: common.MetricMatrix, x: numpy.ndarray, y: numpy.ndarray) -> float:
		"""Compute the distance between two points inside the cube using the metric tensor

		Args:
			metric_tensor:
				 Array[N, N], the component representation of the metric
			x:
				Array[N, 1], the first vector
			y:
				Array[N, 1], the second vector

		Returns:
			float
		"""
		# TODO: why not numpy.sqrt?
		return self.distance_sq(metric_tensor, x, y) ** .5

	def distance_sq(self, metric_tensor: common.MetricMatrix, x: numpy.ndarray, y: numpy.ndarray) -> float:
		"""Compute the distance squared between two points inside the cube using
		the metric tensor, but assuming it is constant

		Args:
			metric_tensor:
				 Array[N, N], the component representation of the metric
			x:
				Array[N, 1], the first vector
			y:
				Array[N, 1], the second vector

		Returns:
			float, the square distance
		"""
		if len(y.shape) > 1:
			return self._distancesq(metric_tensor, x, y)

		delta = x - y
		# FIXME I don't remember the reason for this, but it is
		# probably a terrible idea we should drop the max and see what
		# happens
		# always return floating point epsilon distance
		return max(1e-7, (dot(delta, delta, metric_tensor)))

	def evaluate(self, center: coordinate.Coordinates, scale: float = None, method: str = EvaluationMethod.Deterministic, digits: int = 8, target_match = None) -> numpy.ndarray:
		# TODO coerce to Coordinates when coordinates has been fully array-passthrough
		if target_match is None:
			target_match = self.coord_func.target_match(center)
		center = coordinate.to_array(center)

		# Determine evaluation method
		f = self._method_funcs.get(method.lower(), None)
		if f is None:
			raise ValueError('Unknown evaluation method: {}. Options are: {}'.format(method, list(sorted(self._method_funcs.keys()))))

		g = f(center, target_match=target_match)

		return self._post_process_metric(g, center, scale=scale, method=method, digits=digits, target_match=target_match)

	def _evaluate_hessian(self, center: coordinate.Coordinates, target_match: float = DEFAULT_TARGET_MATCH) -> numpy.ndarray:
		"""Evaluate the metric at a point on the manifold, computing the components of the metric
		and returning as a matrix

		Args:
			center:
				Tuple[float, ...] the coordinates at which to evaluate the metric components
			scale:
				float, default None

		Returns:
			numpy.ndarray of size len(center) x len(center), the metric components at center
		"""
		center = numpy.array(center)
		w_c = self.waveform(center)

		def match(d):
			# t is first parameter by convention
			w2 = self.waveform(center + d[1:])
			return match_minus_1(w_c, w2, self.freq_vec, dt=d[0])

		# Construct Hessian
		import numdifftools
		h = numdifftools.Hessian(match,
								 base_step=self.coord_func.base_step(center),
								 num_steps=40,
								 step_ratio=2,
								 num_extrap=16)

		# Evaluate Hessian at (dt, dlambda) ~ (0, ...)
		gamma = -0.5 * h(numpy.zeros(len(center) + 1))

		return gamma

	def _evaluate_deterministic(self, center: coordinate.Coordinates, target_match: float = DEFAULT_TARGET_MATCH):
		# add in time
		N = len(center)
		c_orig = center
		center = numpy.array([0.] + list(center))
		deltas = self.solve_deltas(center, target_match)

		mt = numpy.zeros((len(center), len(center)))
		mtp = numpy.zeros((N, N))
		w1 = self.waveform_shift(center)

		for i in range(len(center)):
			c2 = center.copy()
			c2[i] += deltas[i]
			w2 = self.waveform_shift(c2)
			# mm = - (self.fft_match(w1, w2) - 1)
			mm = -match_minus_1(w1, w2, self.freq_vec)
			mt[i, i] = (mm) / deltas[i] ** 2

		for i in range(len(center)):
			for j in range(len(center)):
				if j >= i: continue
				c2 = center.copy()
				c2[i] += deltas[i]
				c2[j] += deltas[j]
				w2 = self.waveform_shift(c2)
				mm = -match_minus_1(w1, w2, self.freq_vec)
				mt[i, j] = (mm - mt[i, i] * deltas[i] ** 2 - mt[j, j] * deltas[j] ** 2) / 2 / deltas[i] / deltas[j]
				mt[j, i] = mt[i, j]

		return mt

	def _post_process_metric(self, gamma: numpy.ndarray, center: coordinate.Coordinates, scale: float = None, method: str = EvaluationMethod.Numeric, digits: int = 8, target_match: float = DEFAULT_TARGET_MATCH) -> numpy.ndarray:
		"""Post processing after metric computed

		Args:
			gamma:
				N+1xN+1 array

		Returns:
			NxN array with values coerced
		"""
		N = gamma.shape[0] - 1
		g = numpy.zeros((N, N))

		# project out the time component Owen 2.28 [1]
		for i, j in itertools.product(range(N), range(N)):
			g[i, j] = gamma[i + 1, j + 1] - (gamma[i + 1, 0] * gamma[j + 1, 0] / gamma[0, 0])

		# Crash if there are negative eigen values and potentially impose a minimum
		V, Q = numpy.linalg.eig(g)
		det1 = numpy.product(V)

		largest_num_digits = int(numpy.log10(numpy.abs(center).max())) if (center > 0).any() else 0
		if numpy.any(V < 0.) or numpy.isnan(det1):
			print ("falling back on slower metric calculation")
			if digits > -largest_num_digits:  # FIXME arbitrary need to specify precision not digits...
				g = self.evaluate(numpy.round(center, decimals=digits - 1), scale=scale, method=EvaluationMethod.Numeric, digits=digits - 1)
			else:
				raise EigenvalueError("Unable to resolve negative eigenvalues.")
			V, Q = numpy.linalg.eig(g)
			det1 = numpy.product(V)	

		V[V < self.coord_func.min_eig_val] = self.coord_func.min_eig_val
		V[V < max(V) * MAX_EPSILON_SCALE] = MAX_EPSILON_SCALE * max(V)
		det2 = numpy.product(V)
		# FIXME Check this...
		V *= (det1 / det2) ** (1. / len(V))
		g = numpy.dot(Q, numpy.dot(numpy.diag(V), Q.T))

		if numpy.any(numpy.isnan(g)):
			raise ValueError("nan metric")

		return g

	def solve_deltas(self, center, t):
		w1 = self.waveform_shift(center)
		deltas = []
		for i in range(len(center)):
			dx = numpy.zeros(len(center))
			dx[i] = 1.0

			def _m(delta, dx=dx, w1=w1, center=center, target=t):
				w2 = self.waveform_shift(center + dx * 10 ** delta)
				match_m1 = match_minus_1(w1, w2, self.freq_vec)
				return abs(match_m1 - target + 1.)

			res = optimize.minimize_scalar(_m, bounds=(-10, 0), method='bounded', options={'xatol': 1e-2})
			deltas.append(10 ** res.x)
		return deltas

	def waveform_shift(self, c):
		# By convention time is first coordinate
		w = self.waveform(c[1:])
		if c[0] == 0.:
			return w
		w.data.data = w.data.data * numpy.exp(-2.j * numpy.pi * self.freq_vec * c[0])
		return w

	def fft_match_at_coords(self, c1: coordinate.Coordinates, c2: coordinate.Coordinates) -> float:
		"""Compute fft match at coordinates

		Args:
			c1:
				Coorindates, the first point
			c2:
				Coorindates, the second point

		Returns:
			float
		"""
		return self.fft_match(self.waveform(c1), self.waveform(c2))

	def fft_match(self, w1: lal.COMPLEX16FrequencySeries, w2: lal.COMPLEX16FrequencySeries) -> float:
		"""FFT match between two waveforms

		Args:
			w1:
				COMPLEX16FrequencySeries, the first waveform
			w2:
				COMPLEX16FrequencySeries, the second waveform

		Returns:
			float, the match number
		"""
		self.f_series.data.data[:] = numpy.conj(w1.data.data) * w2.data.data
		lal.COMPLEX16FreqTimeFFT(self.t_series, self.f_series, self.revplan)
		m = (numpy.real(numpy.abs(numpy.array(self.t_series.data.data)).max())
			 / norm_duration(w1.data.data, self.duration)
			 / norm_duration(w2.data.data, self.duration))

		# TODO persist this threshold somewhere
		if m > 1.0000001:
			raise ValueError("Match is greater than 1 : %f" % m)
		return m

	def metric_match(self, metric_tensor: common.MetricMatrix, c1: coordinate.Coordinates, c2: coordinate.Coordinates):
		"""Compute a match using the metric tensor and distance between points

		Args:
			metric_tensor:
				MetricMatrix, the coordinate representation of the metric
			c1:
				Coordinates, the first point
			c2:
				Coordinates, the second point

		Returns:
			float, the match number
		"""
		d2 = self.distance_sq(metric_tensor, c1, c2)
		return numpy.exp(-d2)

	def random_point_at_mismatch(self, g: common.MetricMatrix, center: coordinate.Coordinates, mismatch, mismatch_func=lambda m: m ** .5):
		mat = numpy.linalg.inv(g)
		try:
			L = numpy.linalg.cholesky(mat)
		except numpy.linalg.linalg.LinAlgError as e:
			print(mat, numpy.linalg.det(mat))
			raise e

		while True:
			rp = 2 * numpy.random.rand(g.shape[0]) - 1.0
			rp /= numpy.linalg.norm(rp)
			rp *= mismatch_func(mismatch)
			rp = self.coord_func(numpy.dot(rp, L.T) + center)
			_rp = self.coord_func(rp, inv=True)
			if rp in self.coord_func:
				yield rp

	def waveform(self, coords: coordinate.Coordinates) -> lal.COMPLEX16FrequencySeries:
		"""Method for producing a waveform, this must be defined by subclasses

		Args:
			coords:
				Tuple[float, ...], a tuple of floats

		Returns:
			Frequency Series
		"""
		raise NotImplementedError


def norm_duration(w: lal.COMPLEX16FrequencySeries, duration: int):
	# TODO reconcile this norm with other norm
	return (numpy.real((numpy.conj(w) * w).sum()) / duration) ** .5


def norm(w: numpy.ndarray) -> float:
	"""Compute a trapezoidal norm

	Args:
		w:
			Array, the array for which to compute the norm

	Returns:
		float, the norm
	"""
	# TODO why not numpy.sqrt?
	n = numpy.abs((numpy.conj(w) * w).sum()) ** .5
	return n


def dot(x, y, metric: common.MetricMatrix):
	# TODO reconcile this with inner_product
	return numpy.dot(numpy.dot(x.T, metric), y)


def inner_product(w1: numpy.ndarray, w2: numpy.ndarray) -> float:
	return numpy.abs((numpy.conj(w1) * w2).sum())


# orig
# |xc*y|

# diff way
# (xc - yc) * (x - y)
# (xc*x - xc*y - yc*x + yc*y)
# (2 - [xc*y + (xc*y)c]), eff: z + zc = (a + bi) + (a - bi) = 2a = 2Re(z)
# |2 - 2Re(xc*y)| = 2[1 - Re(xc*y)]


def match_minus_1(w1: lal.COMPLEX16FrequencySeries, w2: lal.COMPLEX16FrequencySeries, freq_vec: numpy.ndarray, dt: float = 0.) -> float:
	try:
		x = numpy.copy(w1.data.data)
		y = numpy.copy(w2.data.data)
		if w1.epoch != w2.epoch or dt:
			y *= numpy.exp(-2.j * numpy.pi * freq_vec * (dt + float(w2.epoch - w1.epoch)))
		y /= norm(y)
		x /= norm(x)
		m = inner_product(x, y)

		return m - 1.0

	# method below is slightly different due to:
	# d1 = x - y
	# mm2 = inner_product(d1, d1)
	# return -0.5 * mm2

	except AttributeError:
		# TODO add logging statement here
		return None


def match_minus_1_at_coords_w_t(c1: coordinate.Coordinates, c2: coordinate.Coordinates, g: Metric, t1: float = 0., t2: float = 0.):
	dt = t2 - t1
	w1 = g.waveform(c1)
	w2 = g.waveform(c2)
	return match_minus_1(w1, w2, g.freq_vec, dt)


def t_factor(t_interval: float, freq_interval: float, freq_high: float, working_length: int) -> numpy.ndarray:
	"""Compute t-factor

	Args:
		t_interval:
		freq_interval:
		freq_high:
		working_length:

	Returns:
		Array
	"""
	freq_range = numpy.arange(working_length) * freq_interval - freq_high
	return numpy.exp(-2j * numpy.pi * freq_range * t_interval)


def volume_element(metric_tensor: common.MetricMatrix) -> float:
	"""Compute volume element of metric matrix

	Args:
		metric_tensor:
			MetricMatrix, the matrix repr of the metric

	Returns:
		float
	"""

	# TODO use numpy ops for abs and sqrt
	return (numpy.linalg.det(metric_tensor)) ** .5


def max_diff_at_edges(g: Metric, center: coordinate.Coordinates, m: numpy.ndarray, target_match: float):
	m_inv = numpy.linalg.inv(m)
	L = numpy.linalg.cholesky(m_inv)

	e1 = L[:, 0]
	e2 = L[:, 1]

	d = numpy.sqrt(1 - target_match)
	p1 = center + d * e1
	p2 = center + d * e2
	p3 = center - d * e1
	p4 = center - d * e2

	diffs = []
	for p in [p1, p2, p3, p4]:
		fft_mm = 1 - g.fft_match_at_coords(center, p)
		metric_mm = 1 - g.metric_match(m, center, p)
		diffs.append((metric_mm - fft_mm) / metric_mm)
	max_diff = numpy.abs(numpy.array(diffs)).max()

	return max_diff
