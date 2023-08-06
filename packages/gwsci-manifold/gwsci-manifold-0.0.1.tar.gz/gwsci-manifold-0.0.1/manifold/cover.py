#!/usr/bin/env python

import itertools

import numpy
from matplotlib import patches
from scipy.spatial import Rectangle
from scipy.special import gamma

from manifold.metric import volume_element


class ManifoldRectangle(Rectangle):
	def __init__(self, mins, maxes, metric, g = None, level = 0, right = False, left = False):
		Rectangle.__init__(self, mins, maxes)
		self.metric = metric
		if g is None and metric is not None:
			self.g = self.metric(self.metric_center)
		elif g is not None:
			self.g = g
		else:
			self.g = numpy.diag(numpy.ones(len(mins)))
		self.edges = numpy.diag(self.size)
		self.level = level
		self.right = right
		self.left = left

	# FIXME this object is technically not immutable so it is a bad idea, so
	# be careful
	def __hash__(self):
		return hash(tuple(list(numpy.round(self.mins, 4)) + list(numpy.round(self.maxes, 4))))

	def __eq__(self, other):
		return numpy.array_equal(self.mins, other.mins) and numpy.array_equal(self.maxes, other.maxes)

	def ball_volume(self, r=0.17):
		# NOTE for templates r = mismatch**.5; So r=0.17 corresponds to
		# a mismatch of 2.9%
		N = len(self.mins)
		return numpy.pi * (N / 2) / gamma(N / 2 + 1) * r ** (N)

	def num_balls(self, r=0.17):
		# NOTE for templates r = mismatch**.5; So r=0.17 corresponds to
		# a mismatch of 2.9%
		# NOTE it is impossible to pack spheres this tightly. This
		# should be considered a lower bound
		return self.proper_volume / self.ball_volume(r=r)

	@property
	def vertices(self):
		for v in itertools.product(*zip(self.mins, self.maxes)):
			yield v

	@property
	def center(self):
		return self.mins + self.size / 2

	@property
	def metric_center(self):
		# NOTE you could override this method to provide a more natural notion of "center" for a given coordinate system
		return self.center

	def split(self, d, split, reuse_g=False):
		"""Produce two hyperrectangles by splitting.
		In general, if you need to compute maximum and minimum
		distances to the children, it can be done more efficiently
		by updating the maximum and minimum distances to the parent.
		Parameters
		----------
		d : int
			Axis to split hyperrectangle along.
		split : float
			Position along axis `d` to split at.
		"""
		mid = numpy.copy(self.maxes)
		mid[d] = split
		less = type(self)(self.mins, mid, self.metric, g=None if not reuse_g else self.g, level = self.level + 1, right = True, left = False)
		mid = numpy.copy(self.mins)
		mid[d] = split
		greater = type(self)(mid, self.maxes, self.metric, g=None if not reuse_g else self.g, level = self.level + 1, right = False, left = True)
		return less, greater

	def bisect(self, d, reuse_g=False):
		return self.split(d, self.center[d], reuse_g=reuse_g)

	def divide(self, d=None, reuse_g=False, aspect_ratios=None):
		if d is None and aspect_ratios is None:
			return self.bisect(numpy.argmax(self.proper_size), reuse_g=reuse_g)
		elif d is None:
			return self.bisect(numpy.argmax(self.proper_size * aspect_ratios), reuse_g=reuse_g)
		else:
			return self.bisect(numpy.argmax(self.proper_size[:d + 1]), reuse_g=reuse_g)

	@property
	def size(self):
		return self.maxes - self.mins

	@property
	def proper_size(self):
		origin = numpy.zeros(len(self.edges))
		return numpy.array([self.metric.distance(self.g, origin, edge) for edge in self.edges])

	@property
	def volume(self):
		return Rectangle.volume(self)

	@property
	def proper_volume(self):
		return volume_element(self.g) * self.volume

	def patch(self, x=0, y=1):
		assert len(self.mins) > 1
		return patches.Rectangle(numpy.array([self.mins[x], self.mins[y]]), self.size[x], self.size[y], edgecolor='k', facecolor='none')

def tmpvol(mm=0.01,N=2):
	return (2 * (mm /N)**.5)**N

class Chart(object):

	def __init__(self, data, parent=None):
		self.left = None
		self.right = None
		self.data = data
		self.parent = parent

	def branch(self, mm=.02, reuse_g_mm=0.0, reuse_g_vol_tol=0.1, constraints=(lambda x: True,), verbose=False, cnt = [0], aspect_ratios = None, min_coord_vol = numpy.inf, min_depth =  11, max_num_templates = 1):
		def inside(r, constraints = constraints):
			out = True
			for constraint in constraints:
				out &= not all(constraint(v) for v in list(r.data.vertices) + [list(r.data.center)])
			return out

		def boundary(r, constraints = constraints):
			out = False
			for constraint in constraints:
				out |= any(constraint(v) for v in r.data.vertices)
			return out

		proper_volume = self.data.proper_volume
		tvol = tmpvol(mm, len(self.data.center))
		Ntmps = max(proper_volume / tvol, self.data.volume / min_coord_vol)
		volratio = (numpy.inf if self.parent is None else self.parent.data.proper_volume) / proper_volume / 2.0
		reuse_g = (proper_volume < tmpvol(reuse_g_mm, len(self.data.center))) and ((1-reuse_g_vol_tol) < volratio < (1+reuse_g_vol_tol))
		if Ntmps > max_num_templates:
			ldat, rdat = self.data.divide(reuse_g=reuse_g, aspect_ratios = aspect_ratios)
			left = Chart(ldat, self)
			right = Chart(rdat, self)
			inl = inside(left);
			inr = inside(right);
			if inl or left.data.level < min_depth:
				self.left = left
				self.left.branch(mm=mm, reuse_g_mm=reuse_g_mm, reuse_g_vol_tol=reuse_g_vol_tol, constraints=constraints, verbose=verbose, cnt = cnt, aspect_ratios = aspect_ratios, min_coord_vol = min_coord_vol, min_depth = min_depth, max_num_templates = max_num_templates)
			if inr or right.data.level < min_depth:
				self.right = right
				self.right.branch(mm=mm, reuse_g_mm=reuse_g_mm, reuse_g_vol_tol=reuse_g_vol_tol, constraints=constraints, verbose=verbose, cnt = cnt, aspect_ratios = aspect_ratios, min_coord_vol = min_coord_vol, min_depth = min_depth, max_num_templates = max_num_templates)
		elif verbose:
			cnt[0] += 1
			if not cnt[0] % 100: print(cnt[0], self.data, volratio)

	def atlas(self):
		if self.left:
			yield from self.left.atlas()
		if self.right:
			yield from self.right.atlas()
		if not self.left and not self.right:
			yield self.data
