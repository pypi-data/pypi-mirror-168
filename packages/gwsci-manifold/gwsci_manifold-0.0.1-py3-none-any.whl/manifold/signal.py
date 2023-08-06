import lal
import numpy
from scipy import interpolate


# FROM https://git.ligo.org/lscsoft/gstlal/-/blob/master/gstlal/python/reference_psd.py#L754
def interpolate_psd(psd, deltaF):
	#
	# no-op?
	#

	if deltaF == psd.deltaF:
		return psd

	#
	# interpolate log(PSD) with cubic spline.  note that the PSD is
	# clipped at 1e-300 to prevent nan's in the interpolator (which
	# doesn't seem to like the occasional sample being -inf)
	#

	psd_data = psd.data.data
	psd_data = numpy.where(psd_data, psd_data, 1e-300)
	f = psd.f0 + numpy.arange(len(psd_data)) * psd.deltaF
	interp = interpolate.splrep(f, numpy.log(psd_data), s=0)
	f = psd.f0 + numpy.arange(round((len(psd_data) - 1)
									* psd.deltaF / deltaF) + 1) * deltaF
	psd_data = numpy.exp(interpolate.splev(f, interp, der=0))

	#
	# return result
	#

	psd = lal.CreateREAL8FrequencySeries(
		name=psd.name,
		epoch=psd.epoch,
		f0=psd.f0,
		deltaF=deltaF,
		sampleUnits=psd.sampleUnits,
		length=len(psd_data)
	)
	psd.data.data = psd_data

	return psd


# From https://git.ligo.org/lscsoft/gstlal/-/blob/master/gstlal-inspiral/python/templates.py#L129
def add_quadrature_phase(fseries, n):
	"""
	From the Fourier transform of a real-valued function of
	time, compute and return the Fourier transform of the
	complex-valued function of time whose real component is the
	original time series and whose imaginary component is the
	quadrature phase of the real part.  fseries is a LAL
	COMPLEX16FrequencySeries and n is the number of samples in
	the original time series.
	"""
	#
	# positive frequencies include Nyquist if n is even
	#

	have_nyquist = not (n % 2)

	#
	# shuffle frequency bins
	#

	positive_frequencies = numpy.array(fseries.data.data)  # work with copy
	positive_frequencies[0] = 0  # set DC to zero
	zeros = numpy.zeros((len(positive_frequencies),), dtype="cdouble")
	if have_nyquist:
		# complex transform never includes positive Nyquist
		positive_frequencies = positive_frequencies[:-1]

	#
	# prepare output frequency series
	#

	out_fseries = lal.CreateCOMPLEX16FrequencySeries(
		name=fseries.name,
		epoch=fseries.epoch,
		f0=fseries.f0,  # caution: only 0 is supported
		deltaF=fseries.deltaF,
		sampleUnits=fseries.sampleUnits,
		length=len(zeros) + len(positive_frequencies) - 1
	)
	out_fseries.data.data = numpy.concatenate(
		(zeros, 2 * positive_frequencies[1:]))

	return out_fseries
