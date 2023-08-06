"""The manifold coordinate utilities can be grouped into three primary categories. First, CoordinateTypes
represent the physical parameter to which given coordinate values (numbers) correspond. Second, Coordinates
represent a set of coordinates, or a point on the coordinate manifold. Third, CoordFuncs convert the values
of a point between different sets of coordinate types, similar to a coordinate transformation.

Consider the example of a simplified compact binary, with two physical parameters: mass 1 and mass 2. We
would declare two coordinate types M1 and M2 representing each physical parameter. We would construct a
point on the manifold by specifying coordinate values and types, such as Coordinates(M1=x, M2=y).
Finally, if we wished to convert to logarithmic mass coordinates, we would declare two additional coordinate
types such as LogM1 and LogM2, then construct a CoordFunc implementing the transformation.
"""

import itertools
from collections import abc
from typing import Iterable, Union, Dict, Any
import numpy


class CoordinateType:
    """A CoordinateType represents the physical quantity associated to point coordinate
    value, such that each dimension of the manifold corresponds to one CoordinateType.

    Attributes:
        key:
            str, the dictionary key to be used for coordinates of this type,
            must specify as a class-level constant when declaring new coordiante
            types as subclasses

    Notes:
        Creating new coordinate types:
            Creation of new coordinate types should be done via subclassing, such that the
            new objects will be proper python types (as opposed to instances of CoordinateType).
            See the example below.

    Examples:
        Simple Sinusoid Waveform: (frequency, phase)
            (dim 1) class Freq(CoordinateType):
                        key = 'frequency_parameter'
            (dim 2) class Phase(CoordinateType):
                        key = 'phase_parameter'
    """


# The type below is a convenient short-hand for common annotations
CoordsDict = Dict[CoordinateType, float]


def is_coord_type(x: Any) -> bool:
    """Determine if the given object is a CoordinateType

    Args:
        x:
            Any, the object to determine if is a CoordinateType

    Returns:
        bool, True if x is a CoordinateType, False otherwise
    """
    return isinstance(x, type) and issubclass(x, CoordinateType)


class Coordinates:
    """Coordinates represents a point on a manifold in a given coordinate system. Consequently,
    each instance is represented by an array of types and an array of values. The values
    are typically floats, whereas the types are typically CoordinateTypes.

    Notes:
        Default coordinate types:
            If no coordinate types are specified, the point is considered in an "unknown" coordinate
            system. As a consequence, errors will be raised when an unknown point is passed to a
            coordinate function for transformation, etc.

    Examples:
        Creating a simple point:
            p = Coordinates(1, 2)
        Creating a point with coordinate types:
            q = Coordinates(1, 2, coord_types=(M1, M2))
    """
    __slots__ = ('_array', '_types')

    def __init__(self, *args, coord_types: Iterable[CoordinateType] = None):
        """Create Coordinates for a point

        Args:
            *args:
                Can either specify a numpy array, an iterable, or a sequence of scalars, e.g.:
                    - Coordinates(1,2)
                    - Coordinates([1,2])
                    - Coordinates(numpy.array([1,2])
            coord_types:
                Iterable[CoordinateType], an optional specification of the types of coordinates
        """
        if len(args) == 1:  # either iterable or array
            if isinstance(args[0], numpy.ndarray):
                self._array = args[0]
            else:
                self._array = numpy.array(args[0])
        else:  # sequence of points
            if not all(isinstance(p, (int, float)) for p in args):
                raise ValueError('If creating coordinates from scalars, all must be numeric. Got: {}'.format(args))
            self._array = numpy.array(args)

        self._types = coord_types

    def __add__(self, other):
        """Define addition of points to pass through to arrays, only if types match"""
        # First coerce other to coordinates object (pass thru if already coordinates)
        try:
            other = to_coordinates(other)
        except Exception as e:
            # Catch any coercion errors as type errors
            raise TypeError('Addition not defined for Coordinates and type {}'.format(type(other))) from e

        # Check that other Coordinates has compatible types
        if self._compatible_types(other):
            return Coordinates(self._array + other._array, coord_types=self._types)
        raise ValueError('Unable to add coordinates with different types {} and {}'.format(self._types, other._types))

    def __getitem__(self, item):
        """Pass through indexing"""
        return self._array.__getitem__(item)

    def __iter__(self):
        """Pass through iteration"""
        return self._array.__iter__()

    def __len__(self):
        """Pass through len"""
        return len(self._array)

    def __repr__(self):
        """Define the string representation of a Coordinate point"""
        if self._types is not None:
            r = ['{}={}'.format(t.key, str(c)) for c, t in zip(self._array, self._types)]
        else:
            r = [str(c) for c in self._array]
        return 'Coordinate({})'.format(', '.join(r))

    def _compatible_types(self, other):
        """Helper function for determining if these coordinates have compatible
        types with another set of coordinates, a necessary step before binary operations
        """
        if not isinstance(other, Coordinates):
            return False
        if self._types is not None and other._types is not None:
            return self._types == other._types
        return True

    @property
    def shape(self):
        return self._array.shape


def to_coordinates(x: Union[Iterable, numpy.ndarray, Coordinates]) -> Coordinates:
    """Coerce an object to a Coordinates instance if possible,
    helpful when adding the Coordinate class abstractions

    Args:
        x:
            Iterable, array, or Coordinates, The object to coerce to Coordinates if possible

    Returns:
        Coordinates, the coerced coordinates
    """
    if isinstance(x, Coordinates):
        return x

    if isinstance(x, (numpy.ndarray, abc.Iterable)):
        return Coordinates(x)

    raise ValueError('Unable to coerce type {} to Coordinates, {}'.format(type(x), x))


def to_array(x: Union[Iterable, numpy.ndarray, Coordinates]) -> numpy.ndarray:
    """Utility for coercing object to an array if possible,
    helpful when removing the Coordinate class abstractions

    Args:
        x:
            Iterable, array, or Coordinates, the object to be coerced to an array if possible

    Returns:
        numpy.ndarray, the coerced array
    """
    if isinstance(x, numpy.ndarray):
        return x

    if isinstance(x, Coordinates):
        return x._array

    return numpy.array(x)


class CoordFunc(object):
    """Coordinate function

    """
    _STANDARD_COORD_TYPES = ()  # this will be populated by subclasses
    TO_TYPES = ()  # this will be populated by subclasses
    FROM_TYPES = ()  # this will be populated by subclasses

    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        kwargs = self._normalize_coorddict(kwargs)
        self._set_bounds(kwargs)

        self.mins = [self.from_bounds[k][0] for k in self.FROM_TYPES]
        self.maxes = [self.from_bounds[k][1] for k in self.FROM_TYPES]

    def to_dict(self):
        return self.__kwargs.copy()

    def __call__(self, c: Coordinates, inv: bool = False):
        """Method to convert coordinates FROM -> TO. The inverse (inv=True)
        transform converts TO -> FROM.
        """
        raise NotImplementedError

    def __contains__(self, params: CoordsDict):
        if params is None:
            return False

        if self.from_bounds is None or self.to_bounds is None:
            return True

        if set(self.TO_TYPES) == set(params.keys()):
            values = numpy.array([params[ct] for ct in self.TO_TYPES])
            bounds = self.to_bounds
        elif set(self.FROM_TYPES) == set(params.keys()):
            values = numpy.array([params[ct] for ct in self.FROM_TYPES])
            bounds = self.from_bounds
        else:
            raise ValueError('Cannot determine if coord func contains point with keys {}'.format(list(params.keys())))

        if any(numpy.isnan(values)):
            return False

        if any(numpy.isinf(values)):
            return False

        for k, v in params.items():
            if k in bounds and (v < bounds[k][0] or v > bounds[k][1]):
                return False
        return True

    def _set_bounds(self, bounds: dict):
        if set(self.TO_TYPES) == set(bounds.keys()):
            self.to_bounds = bounds

            min_coords = {k: self.to_bounds[k][0] for k in self.to_bounds}
            max_coords = {k: self.to_bounds[k][1] for k in self.to_bounds}

            from_min_coords = self(min_coords, inv=True)
            from_max_coords = self(max_coords, inv=True)

            if from_min_coords.shape and from_max_coords.shape:
                self.from_bounds = dict(zip(self.FROM_TYPES, zip(list(from_min_coords), list(from_max_coords))))
            else:  # single coordinate, array has no len
                self.from_bounds = {self.FROM_TYPES[0]: [float(from_min_coords), float(from_max_coords)]}
        elif set(self.FROM_TYPES) == set(bounds.keys()):
            self.from_bounds = bounds

            min_coords = numpy.array([self.from_bounds[k][0] for k in self.from_bounds])
            max_coords = numpy.array([self.from_bounds[k][1] for k in self.from_bounds])

            to_min_coords = self(min_coords)
            to_max_coords = self(max_coords)

            self.to_bounds = {t: [to_min_coords[t], to_max_coords[t]] for t in self.TO_TYPES}
        else:
            raise ValueError('Unable to set bounds, must specify either a set of domain or codomain bounds.')

    def _normalize_coorddict(self, d: dict, inv: bool = False) -> CoordsDict:
        if inv:
            key_type_lookup = {t.key: t for t in self._STANDARD_COORD_TYPES}
        else:
            d_keys = set(_d.key if is_coord_type(_d) else _d for _d in d.keys())
            if d_keys.issubset(set(t.key for t in self.TO_TYPES)):
                key_type_lookup = {t.key: t for t in self.TO_TYPES}
            elif d_keys.issubset(set(t.key for t in self.FROM_TYPES)):
                key_type_lookup = {t.key: t for t in self.FROM_TYPES}
            else:
                raise ValueError('Can only normalize dicts whose keys are subsets of either TO_TYPES or FROM_TYPES, got: {}'.format(d_keys))
        cd = {}
        for k, v in d.items():
            if is_coord_type(k):
                cd[k] = d[k]
            else:
                cd[key_type_lookup[k]] = d[k]
        return cd

    def dx(self, c: Coordinates):
        raise NotImplementedError

    def grid(self, **kwargs):
        """kwargs are key value pairs of coordinates and the number of points to
        generate. From python 3.6 the order will be preserved, e.g.,

        grid(m1 = 100, m2 = 100, S1z = 10, S2z = 10)
        """
        kwargs = self._normalize_coorddict(kwargs)
        assert not (set(kwargs) - set(self.from_bounds))
        vecs = [numpy.linspace(self.from_bounds[p][0], self.from_bounds[p][1], kwargs[p]) for p in kwargs]
        for coord in itertools.product(*vecs):
            yield coord

    def random(self):
        raise NotImplementedError

    @property
    def base_step(self):
        raise NotImplementedError

    def min_scale(self, coords):
        raise NotImplementedError
