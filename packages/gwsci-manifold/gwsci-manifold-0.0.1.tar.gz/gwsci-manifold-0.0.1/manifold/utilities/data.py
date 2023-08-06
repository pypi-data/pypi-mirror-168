"""Data loading and formatting utilities. This module broadly contains several categories of utilities
including: reading and writing data files, coercing datatypes of common columns, and parsing specific
data format strings.
"""

import datetime
import json
import os
import pathlib
import pwd
import shutil
import sys
import tempfile
from typing import Union, Any, Iterable

import h5py
import lal
import numpy
from lal import series, LIGOTimeGPS
from ligo import segments
from ligo.lw import utils as ligolw_utils, table

PACKAGE_ROOT = pathlib.Path(__file__).parent.parent
DATA_ROOT = PACKAGE_ROOT.parent / 'tests' / 'data'
SCRIPT_ROOT = PACKAGE_ROOT.parent / 'bin'
TREEBANK_PSD = DATA_ROOT / 'psd_for_treebank.xml.gz'
O3A_PSD = DATA_ROOT / 'REF.xml.gz'


################################################################################
#                              NUMPY ARRAY TYPES                               #
################################################################################

class LALDTypes:
	"""Additional data types for numpy arrays
	"""
	GPSType = numpy.dtype([('s', numpy.int32), ('ns', numpy.int32)])  # Stores a LIGOTimeGPS
	GPSSegListType = numpy.dtype([('start', GPSType), ('end', GPSType)])  # Stores a segment list of LIGOTimeGPS

	# Stores a mass event (without injections)
	EventType = numpy.dtype([
		('id', 'S24'),
		('trig_start', GPSType),
		('trig_stop', GPSType),
		('data_epoch', GPSType),
		('data_length', numpy.int32),
		('run_time', numpy.float32),
		('m1', numpy.float),
		('m2', numpy.float),
		('S1z', numpy.float),
		('S2z', numpy.float),
		('snr', numpy.float32),
		('L', numpy.float32),
		('far', numpy.float32),
		('fmerg', numpy.float32),
		('H1_snr', numpy.float32),
		('L1_snr', numpy.float32),
		('V1_snr', numpy.float32),
		('K1_snr', numpy.float32),
		('H1_chisq', numpy.float32),
		('L1_chisq', numpy.float32),
		('V1_chisq', numpy.float32),
		('K1_chisq', numpy.float32),
		('H1_chisq_dof', numpy.float32),
		('L1_chisq_dof', numpy.float32),
		('V1_chisq_dof', numpy.float32),
		('K1_chisq_dof', numpy.float32),
		('H1_perp_snr', numpy.float32),
		('L1_perp_snr', numpy.float32),
		('V1_perp_snr', numpy.float32),
		('K1_perp_snr', numpy.float32),
		('H1_L', numpy.float32),
		('L1_L', numpy.float32),
		('V1_L', numpy.float32),
		('K1_L', numpy.float32),
		('H1_fstd', numpy.float32),
		('L1_fstd', numpy.float32),
		('V1_fstd', numpy.float32),
		('K1_fstd', numpy.float32),
		('H1_time', numpy.float64),
		('L1_time', numpy.float64),
		('V1_time', numpy.float64),
		('K1_time', numpy.float64),
		('H1_phase', numpy.float32),
		('L1_phase', numpy.float32),
		('V1_phase', numpy.float32),
		('K1_phase', numpy.float32)
	])

	# Stores a mass sim_inspiral row
	# FIXME, we probably want to bring in other parameters here
	SimType = numpy.dtype([
		("time_geocent", GPSType),
		("h_end_time", GPSType),
		("l_end_time", GPSType),
		("v_end_time", GPSType),
		("k_end_time", GPSType),
		("mass1", numpy.float),
		("mass2", numpy.float),
		("spin1x", numpy.float),
		("spin1y", numpy.float),
		("spin1z", numpy.float),
		("spin2x", numpy.float),
		("spin2y", numpy.float),
		("spin2z", numpy.float),
		("distance", numpy.float),
		("inclination", numpy.float),
		("coa_phase", numpy.float),
		("H1_snr", numpy.float32),
		("L1_snr", numpy.float32),
		("V1_snr", numpy.float32),
		("K1_snr", numpy.float32),
		("network_snr", numpy.float32)
	])

	# Stores a mass event that is the result of an injection
	InjectionEventType = numpy.dtype([("event", EventType), ("sim", SimType)])

	@classmethod
	def r8ftype(cls, N):
		"""Stores and arbitrary length REAL8FrequencySeries"""
		return numpy.dtype([
			('__type__', 'S8'),
			('name', 'S256'),
			('epoch', cls.GPSType),
			('f0', 'f8'),
			('deltaF', 'f8'),
			('sampleUnits', 'S256'),
			('length', numpy.int),
			('data', 'f8', N),
		])


################################################################################
#                       NUMPY ARRAY ENCODING AND DECODING                      #
################################################################################


class EncodingError(ValueError):
	"""Base class for encoding related errors"""


def seglist_to_array(seglist: segments.segmentlist) -> numpy.ndarray:
	"""Convert a SegList to a numpy array

	Args:
		seglist:
			segmentlist, the segment list to convert to a numpy array

	Returns:
		numpy.ndarray, the coerced array
	"""
	return numpy.array([
		(numpy.array((s[0].gpsSeconds, s[0].gpsNanoSeconds), dtype=LALDTypes.GPSType),
		 numpy.array((s[1].gpsSeconds, s[1].gpsNanoSeconds), dtype=LALDTypes.GPSType))
		for s in seglist], LALDTypes.GPSSegListType)


def array_to_seglist(a: numpy.ndarray) -> segments.segmentlist:
	"""Convert a numpy array to a LIGO segmentlist

	Args:
		a:
			numpy.ndarray, the array to convert to a LIGO segmentlist

	Returns:
		segmentlist
	"""
	return segments.segmentlist([(np2gps(x['start']), np2gps(x['end'])) for x in a])


def gps_to_array(gps: LIGOTimeGPS) -> numpy.ndarray:
	"""Convert a LIGOTimeGPS to a numpy array

	Args:
		gps:
			LIGOTimeGPS, the GPS time to convert to an array

	Returns:
		numpy.ndarray
	"""
	return numpy.array([(gps.gpsSeconds, gps.gpsNanoSeconds)], dtype=gpstype)


def array_to_gps(a: numpy.ndarray) -> LIGOTimeGPS:
	"""Convert a numpy array to a LIGOTimeGPS

	Args:
		a:
			numpy.ndarray

	Returns:
		LIGOTimeGPS
	"""
	return LIGOTimeGPS(int(a['s']), int(a['ns']))


def r8f_to_array(o: lal.REAL8FrequencySeries) -> numpy.ndarray:
	"""Convert a LIGO REAL8FrequencySeries to a numpy array

	Args:
		o:
			lal.REAL8FrequencySeries, the series to convert into a numpy array

	Returns:
		numpy.ndarray
	"""
	return numpy.array(('r8f', o.name, gps_to_array(o.epoch), o.f0, o.deltaF, o.sampleUnits, o.data.length, tuple(o.data.data)),
					   dtype=LALDTypes.r8ftype(o.data.length))


def dict_to_r8f(o: dict) -> lal.REAL8FrequencySeries:
	"""Convert a dict to a REAL8FrequencySeries

	Args:
		o:
			dict, the object to convert into a REAL8FrequencySeries

	Returns:
		REAL8FrequencySeries
	"""
	out = lal.CreateREAL8FrequencySeries(
		name=str(o["name"]),
		epoch=array_to_gps(o["epoch"]),
		f0=float(o["f0"]),
		deltaF=float(o["deltaF"]),
		sampleUnits=lal.Unit(o["sampleUnits"].item().from_array('utf-8')),
		length=int(o["length"].item()))
	out.data.data[:] = o["data"][:]
	return out


def dict_to_array(d: dict) -> numpy.ndarray:
	"""Convert a dict into a numpy array

	Args:
		d:
			dict, the dict to convert into a numpy array

	Returns:
		numpy.ndarray
	"""
	dtype = []
	arr = []
	for k, v in d.items():
		_arr = to_array(v)
		dtype.append((k, _arr.dtype, _arr.shape))
		arr.append(_arr)
	dtype = numpy.dtype(dtype)
	return numpy.array(tuple(arr), dtype=dtype)


def gps_to_str(t: LIGOTimeGPS) -> str:
	"""Convert a LIGO GPS Time to a str

	Args:
		t:
			LIGOTimeGPS, time to convert to string

	Returns:
		str
	"""
	return "%d.%09d" % (t.gpsSeconds, t.gpsNanoSeconds)


def str_to_gps(k: str) -> LIGOTimeGPS:
	"""Convert str to LIGO Time GPS

	Args:
		k:
			str, the string to convert into LIGOTimeGPS

	Returns:
		str, the converted string
	"""
	s, ns = k.split(".")
	return LIGOTimeGPS(int(s), int(ns))


def sim_inspiral_to_dict(sim: table.Table, snr: float = None) -> dict:
	"""This is meant to basically give the minimum parameters to match an injection to one in
	a proper LIGOLW file. That should be taken as the source of truth

	Args:
		sim:
			SimInspiralTable
		snr:
			float, default None

	Notes:
		 TODO: decide what we are doing with data formats

	Returns:
		dict
	"""
	out = {k: getattr(sim, k) for k in ("time_geocent", "mass1", "mass2", "spin1x", "spin1y", "spin1z", "spin2x", "spin2y", "spin2z", "distance", "inclination", "coa_phase")}
	if snr is not None:
		out['snr'] = snr
	# FIXME there is no k_end_time columns, we need to switch this to the ligolw methods
	for k in ('h_end_time', 'l_end_time', 'v_end_time'):  # , 'k_end_time'):
		out[k] = LIGOTimeGPS(getattr(sim, k), getattr(sim, '%s_ns' % k))
	return out


def to_array(o: Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, Any]) -> numpy.ndarray:
	"""Convert an arbitrary object to a numpy array

	Args:
		o:
			Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, Any], the object to convert to a numpy array

	Returns:
		numpy.ndarray
	"""
	if isinstance(o, dict):
		return dict_to_array(o)
	elif isinstance(o, segments.segmentlist):
		return seglist_to_array(o)
	elif isinstance(o, LIGOTimeGPS):
		return gps_to_array(o)
	elif isinstance(o, lal.REAL8FrequencySeries):
		return r8f_to_array(o)
	elif isinstance(o, str):
		return numpy.array(o, 'S')
	else:
		# NOTE numpy will encode a lot of things, it doesn't guarantee h5py can write them to disk
		try:
			return numpy.array(o)
		except numpy.VisibleDeprecationWarning as e:
			raise EncodingError('Error encoding object {}'.format(str(o))) from e


def from_array(x: numpy.ndarray) -> Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, numpy.ndarray]:
	"""Convert a numpy array into a decoded object based on the dtype

	Args:
		x:
			numpy.ndarray, the array to decode

	Notes:
		Order: NOTE THE ORDER MATTERS! you need to check the generic dtype.names and shape == () at the end or stuff will break

	Returns:
		Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, numpy.ndarray], the decoded object
	"""
	if x.dtype == LALDTypes.GPSSegListType:
		return array_to_seglist(x)
	if x.dtype == LALDTypes.GPSType:
		return array_to_gps(x)
	if x.dtype.names is not None and "__type__" in x.dtype.names and x['__type__'].item().from_array('utf-8') == "r8f":
		return dict_to_r8f(x)
	if x.dtype in (LALDTypes.EventType, LALDTypes.SimType, LALDTypes.InjectionEventType):
		return x
	if x.dtype.names is not None:
		return {k: from_array(x[k]) for k in x.dtype.names}
	if x.dtype.char == "S":
		return x.item().decode('utf-8')
	if x.shape == ():
		return x.item()
	else:
		return x


class JSONEncoder(json.JSONEncoder):
	"""JSON Encoder that can handle LIGOTimeGPS"""

	def default(self, obj):
		if isinstance(obj, LIGOTimeGPS):
			return "%d.%d" % (obj.gpsSeconds, obj.gpsNanoSeconds)
		return json.JSONEncoder.default(self, obj)


################################################################################
#                            FILE READING UTILITIES                            #
################################################################################

DEFAULT_RECORD_ENV_VARS = (
	"GI_TYPELIB_PATH",
	"GST_PLUGIN_PATH",
	"LAL_DATA_PATH",
	"LAL_PATH",
	"LD_LIBRARY_PATH",
	"LIBRARY_PATH",
	"PATH",
	"PKG_CONFIG_PATH",
	"PYTHONPATH"
)


def record_env(env_vars: Iterable[str] = DEFAULT_RECORD_ENV_VARS) -> dict:
	"""Capture environment variables into a new dict

	Args:
		env_vars:
			Iterable[str], a collection of env variable names

	Returns:
		dict
	"""
	info = {}
	info.update({k: v for k, v in os.environ.items() if k in env_vars})
	info.update({k: os.uname()[i] for (i, k) in enumerate(("sysname", "nodename", "release", "version", "machine"))})
	info.update({"cwd": os.getcwd()})
	info.update({"pid": os.getpid()})
	info.update({"user": pwd.getpwuid(os.geteuid())[0]})
	info.update({"cmd": " ".join(sys.argv)})
	return {str(datetime.datetime.now()): info}


def read_psd(path: Union[str, pathlib.Path], detector: str, verbose: bool = False) -> lal.REAL8FrequencySeries:
	"""Load PSD (power spectral density) from a file for a particular detector

	Args:
		path:
			str or Path, the location of the data file
		detector:
			str, the name of the detector for which to extract data from path
		verbose:
			bool, default False, if True load verbosely using ligo.lw.utils.load_filename(..., verbose=True)

	Returns:
		REAL8FrequencySeries, the psd series
	"""
	path = path.as_posix() if isinstance(path, pathlib.Path) else path
	raw_data = ligolw_utils.load_filename(path, verbose=verbose, contenthandler=series.PSDContentHandler)
	return series.read_psd_xmldoc(raw_data)[detector]


def _read_h5(file: Union[h5py.Dataset, dict], ignore_groups=()) -> Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, numpy.ndarray]:
	if isinstance(file, h5py.Dataset):
		x = numpy.array(file)
		if file.attrs:
			return {"__attrs__": {k: from_array(v) for k, v in file.attrs.items()}, "__data__": from_array(x)}
		else:
			return from_array(x)

	# otherwise we descend
	out = {}
	for k, v in tuple(file.items()):
		if k in ignore_groups:
			continue
		else:
			out[k] = _read_h5(v, ignore_groups)
	return out


def read_h5(filename: str, group: str = None, ignore_groups=()):
	"""Read an hdf5 file and decode the corresponding data

	Args:
		filename:
			str, the filename to write out
		group:
			str, default None, if given the subpath in the hdf5 file
		ignore_groups:
			Tuple, default empty tuple, the list of groups to ignore when converting hdf5 file

	Returns:

	"""
	try:
		with h5py.File(filename, 'r') as f:
			if group is None:
				return _read_h5(f, ignore_groups=ignore_groups)
			else:
				return _read_h5(f[group], ignore_groups=ignore_groups)
	except OSError:
		return {}


def _write_h5(file: h5py.File, x: Union[dict, segments.segmentlist, LIGOTimeGPS, lal.REAL8FrequencySeries, str, numpy.ndarray]):
	for k in x:
		if isinstance(x[k], dict):
			# handle special case where dict is just used to annotate a sngl dataset
			# NOTE: assumes that what is in __data__ is already serializable
			if "__attrs__" in x[k] and (set(x[k]) - set(("__attrs__",)) == set(("__data__",))):
				d = file.create_dataset(str(k), data=x[k]["__data__"])
				for k, v in x[k]["__attrs__"].items():
					d.attrs[k] = to_array(v)
			# FIXME this could probably be supported fairly easily
			elif "__attrs__" in x[k]:
				raise ValueError("Currently only attribute for data sets are supported and are given in the form {'__attrs__': <dict>, '__data__': <something directly encodable>}")
			else:
				g = file.create_group(str(k))
				_write_h5(g, x[k])
		else:
			file.create_dataset(str(k), data=to_array(x[k]))


def write_h5(filename: str, x: object):
	"""Write a hdf5 file

	Args:
		filename:
			str, the path to the file to be written
		x:
			object, the object to be converted to hdf5 and written out

	Returns:
		None, writes a file
	"""
	if '__process' in x:
		x['__process'].update(record_env())
	else:
		x['__process'] = record_env()
	with h5py.File(filename, "w") as f:
		_write_h5(f, x)


def snapshot_h5(filename: str, x: object):
	"""Create an hdf5 snapshot file

	Args:
		filename:
			str, the path to the file to be written
		x:
			object, the object to be converted to hdf5 and written out

	Returns:
		None, writes out a file
	"""
	f, tmpfname = tempfile.mkstemp()
	os.close(f)
	write_h5(tmpfname, x)
	shutil.move(tmpfname, filename)
