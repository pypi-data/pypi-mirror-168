"""Simple sources

"""
from typing import Union

import lal
import numpy

import manifold
from manifold import metric, signal, coordinate


# Define CBC Coordinate Types

class F(coordinate.CoordinateType):
	"""frequency"""
	key = 'f'


class Omega(coordinate.CoordinateType):
	"""angular frequency"""
	key = 'omega'


class Phi(coordinate.CoordinateType):
	"""Phase angle"""
	key = 'phi'


class Lambda(coordinate.CoordinateType):
	"""decay coefficient"""
	key = 'lam'


class DampedSinCoordFunc(coordinate.CoordFunc):
	_STANDARD_COORD_TYPES = (Omega, Phi, Lambda)

	def dx(self, c: coordinate.Coordinates):
		return metric.DELTA * numpy.ones(len(c))

	@property
	def base_step(self):
		return .01

	def min_scale(self, c: coordinate.Coordinates):
		return sum(c[:2]) * 1e-4


class OmegaLambda(DampedSinCoordFunc):
	TO_TYPES = (Omega, Lambda)
	FROM_TYPES = (Omega, Lambda)

	def __call__(self, c: Union[coordinate.Coordinates, coordinate.CoordsDict], inv: bool = False):
		if inv:
			c = self._normalize_coorddict(c)
			w, l = c[Omega], c[Lambda]
			return numpy.array([w, l])
		else:
			w = c[..., 0]
			l = c[..., 1]
			try:
				return {Omega: float(w),
						Lambda: float(l)}
			except (ValueError, TypeError):  # must be array
				return [{Omega: w, Lambda: l} for (w, l) in numpy.array([w, l]).T]

	def base_step(self, c: coordinate.Coordinates):
		return min(1e-4 * sum(c) ** 2, .3 * c[0], .3 * c[1])

	def min_scale(self, c: coordinate.Coordinates):
		return sum(c) * 5e-4


class DampedSinMetric(manifold.metric.Metric):
	"""Class to numerically evaluate the damped sine waveforms

	"""
	WAVEFORM_COORDS = (Omega, Lambda)
	WAVEFORM_COORD_DEFAULTS = {Lambda: 1.}

	def __init__(self, psd, coord_func, flow=15.0, fhigh=512., ):
		manifold.metric.Metric.__init__(self, psd, coord_func, flow, fhigh)

	def waveform(self, c: coordinate.Coordinates):
		# Generalize to different waveform coords
		parameters = self.coord_func(c)

		try:
			parameters['freq_vec'] = self.freq_vec[::2]
			parameters = self._normalize_waveform_params(parameters)

			raw = damped_sin_waveform_freqd(**parameters)
			fseries = lal.CreateCOMPLEX16FrequencySeries(
				name='DampedSin',
				epoch=lal.LIGOTimeGPS(0),
				f0=self.freq_low,
				deltaF=self.freq_interval,
				sampleUnits=lal.Unit('s strain'),
				length=len(raw),
			)
			fseries.data.data[:] = raw
			# TODO fix error with whitening
			lal.WhitenCOMPLEX16FrequencySeries(fseries, self.psd)
			fseries = signal.add_quadrature_phase(fseries, self.working_length)

		except RuntimeError:
			return None
		return fseries


def damped_sin_waveform_timed(ts: numpy.ndarray, omega: float, phi: float, lam: float):
	return numpy.exp(- lam * ts) * numpy.sin(omega * ts + phi)


def damped_sin_waveform_freqd(freq_vec: numpy.ndarray, omega: float, lam: float):
	"""

	Args:
		freq_vec:
		omega:
		lam:

	Notes:
		Reference table: https://uspas.fnal.gov/materials/11ODU/FourierTransformPairs.pdf

	Returns:

	"""
	return omega / (omega ** 2 + (lam + 1j * freq_vec) ** 2)


coord_funcs = {
	# Tested coord funcs
	"omega_lam": OmegaLambda,
}
