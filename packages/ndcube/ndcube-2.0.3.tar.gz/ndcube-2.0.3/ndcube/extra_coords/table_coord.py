import abc
import copy
from numbers import Integral
from collections import defaultdict

import astropy.units as u
import gwcs
import gwcs.coordinate_frames as cf
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.modeling import models
from astropy.modeling.models import tabular_model
from astropy.modeling.tabular import _Tabular
from astropy.time import Time
from astropy.wcs.wcsapi.wrappers.sliced_wcs import combine_slices, sanitize_slices

__all__ = ['TimeTableCoordinate', 'SkyCoordTableCoordinate', 'QuantityTableCoordinate']


class Length1Tabular(_Tabular):
    _input_units_allow_dimensionless = True
    _has_inverse_bounding_box = True
    _separable = True

    n_inputs = 1
    n_outputs = 1

    lookup_table = np.zeros([1])
    points = np.zeros([1])

    def __init__(self, points=None, lookup_table=None, point_width=None, value_width=None,
                 method='linear', bounds_error=True, fill_value=np.nan, **kwargs):
        """Create a Length-1 1-D Tabular model.

        Parameters
        ----------
        points: `astropy.units.Quantity`
            The point/index of the lookup table.
        lookup_table: `astropy.units.Quantity`
            The real world value at the point in the lookup table.
        point_width: `astropy.units.Quantity`
            The width of the point in point units.
        value_width: `astropy.units.Quantity`
            The width of the point in world units.
            Equivalent of CDELT in FITS-WCS.

        Other parameters are defined by the parent class.
        """
        if len(lookup_table) != 1:
            raise ValueError("lookup_table must have length 1.")
        super().__init__(points=points, lookup_table=lookup_table, method=method,
                         bounds_error=bounds_error, fill_value=fill_value, **kwargs)
        self._value_width = value_width  # Width of point in world units.
        if self._value_width is None:
            self._value_width = 0 * self.lookup_table.unit
        self._point_width = point_width  # Width of point in point units.
        if self._point_width is None:
            self._point_width = 1 * self.points[0].unit

    def evaluate(self, x):
        output = np.full(x.shape, self.fill_value)
        diff = abs(x - self.points[0])
        margin = self._point_width / 2
        if margin.value == 0:
            idx = diff == margin
        else:
            idx = np.logical_and(diff >= -1 * margin, diff < margin)
        output[idx] = self.lookup_table[0].value
        return output * self.lookup_table.unit

    @property
    def inverse(self):
        return InverseLength1Tabular(points=self.points[0], lookup_table=self.lookup_table,
                                     point_width=self._point_width, value_width=self._value_width,
                                     method=self.method, bounds_error=self.bounds_error,
                                     fill_value=self.fill_value)


class InverseLength1Tabular(Length1Tabular):
    """A Length1Tabular class whose forward transform goes from lookup table value to point.

    This is the opposite direction to Length1Tabular.
    """
    def __init__(self, **kwargs):
        # Same inputs as Length1Tabular
        points = kwargs.pop("points", None)
        lookup_table = kwargs.pop("lookup_table", None)
        point_width = kwargs.pop("point_width", None)
        value_width = kwargs.pop("value_width", None)
        super().__init__(points=lookup_table, lookup_table=points,
                         point_width=value_width, value_width=point_width, **kwargs)

    def evaluate(self, x):
        # When calling evaluate with a bounding box, astropy strips the units.
        x = u.Quantity(x, unit=self.input_units['x'], copy=False)
        return super().evaluate(x)


def _generate_generic_frame(naxes, unit, names=None, physical_types=None):
    """
    Generate a simple frame, where all axes have the same type and unit.
    """
    axes_order = tuple(range(naxes))

    name = None
    axes_type = "CUSTOM"

    if isinstance(unit, (u.Unit, u.IrreducibleUnit, u.CompositeUnit)):
        unit = tuple([unit] * naxes)

    if all([u.m.is_equivalent(un) for un in unit]):
        axes_type = "SPATIAL"

    if all([u.pix.is_equivalent(un) for un in unit]):
        name = "PixelFrame"
        axes_type = "PIXEL"

    axes_type = tuple([axes_type] * naxes)

    return cf.CoordinateFrame(naxes, axes_type, axes_order, unit=unit,
                              axes_names=names, name=name, axis_physical_types=physical_types)


def _generate_tabular(lookup_table, interpolation='linear', points_unit=u.pix, **kwargs):
    """
    Generate a Tabular model class and instance.
    """
    if not isinstance(lookup_table, u.Quantity):
        raise TypeError("lookup_table must be a Quantity.")  # pragma: no cover

    ndim = lookup_table.ndim
    TabularND = tabular_model(ndim, name=f"Tabular{ndim}D")

    # The integer location is at the centre of the pixel.
    points = [(np.arange(size) - 0) * points_unit for size in lookup_table.shape]
    if len(points) == 1:
        points = points[0]

    kwargs = {'bounds_error': False,
              'fill_value': np.nan,
              'method': interpolation,
              **kwargs}

    if len(lookup_table) == 1:
        t = Length1Tabular(points, lookup_table, **kwargs)
    else:
        t = TabularND(points, lookup_table, **kwargs)

        # TODO: Remove this when there is a new gWCS release
        # Work around https://github.com/spacetelescope/gwcs/pull/331
        t.bounding_box = None

    return t


def _generate_compound_model(*lookup_tables, mesh=True):
    """
    Takes a set of quantities and returns a ND compound model.
    """
    model = _generate_tabular(lookup_tables[0])
    for lt in lookup_tables[1:]:
        model = model & _generate_tabular(lt)

    if mesh:
        return model

    # If we are not meshing the inputs duplicate the inputs across all models
    mapping = list(range(lookup_tables[0].ndim)) * len(lookup_tables)
    return models.Mapping(mapping) | model


def _model_from_quantity(lookup_tables, mesh=False):
    if len(lookup_tables) > 1:
        return _generate_compound_model(*lookup_tables, mesh=mesh)

    return _generate_tabular(lookup_tables[0])


class BaseTableCoordinate(abc.ABC):
    """
    A Base LookupTable contains a single lookup table coordinate.

    This can be multi-dimensional, to support use cases for coupled dimensions,
    such as SkyCoord, or a 3D grid of distances where three 1D lookup tables
    are supplied for each of the axes. The upshot of this is that each
    BaseLookupTable has only one gWCS frame.

    The contrasts with LookupTableCoord which can contain multiple physical
    coordinates, meaning it can have multiple gWCS frames.
    """
    def __init__(self, *tables, mesh=False, names=None, physical_types=None):
        self.table = tables
        self.mesh = mesh
        self.names = names if not isinstance(names, str) else [names]
        self.physical_types = physical_types if not isinstance(physical_types, str) else [physical_types]
        self._dropped_world_dimensions = defaultdict(list)
        self._dropped_world_dimensions["world_axis_object_classes"] = dict()

    @abc.abstractmethod
    def __getitem__(self, item):
        pass  # pragma: no cover

    def __and__(self, other):
        if not isinstance(other, BaseTableCoordinate):
            return NotImplemented

        if isinstance(other, MultipleTableCoordinate):
            # By returning NotImplemented here we trigger python calling
            # __rand__ on LookupTableCoord, which will work if other is a
            # BaseTableCoordinate but fail otherwise
            return NotImplemented

        return MultipleTableCoordinate(self, other)

    def __str__(self):
        header = f"{self.__class__.__name__} {self.names or ''} {self.physical_types or '[None]'}:"
        content = str(self.table).lstrip('(').rstrip(',)')
        if len(header) + len(content) >= np.get_printoptions()['linewidth']:
            return '\n'.join((header, content))
        else:
            return ' '.join((header, content))

    def __repr__(self):
        return f"{object.__repr__(self)}\n{self}"

    @property
    @abc.abstractmethod
    def n_inputs(self):
        """
        Number of pixel dimensions in this table.
        """

    @abc.abstractmethod
    def is_scalar(self):
        """
        Return a boolean if this coordinate is a scalar.

        This is used by `.MultipleTableCoordinate` and `.ExtraCoords` to know
        if the dimension has been "dropped".
        """

    @property
    @abc.abstractmethod
    def frame(self):
        """
        Generate the Frame for this LookupTable.
        """

    @property
    @abc.abstractmethod
    def model(self):
        """
        Generate the Astropy Model for this LookupTable.
        """

    @property
    def wcs(self):
        """
        A gWCS object representing all the coordinates.
        """
        model = self.model
        return gwcs.WCS(forward_transform=model,
                        input_frame=_generate_generic_frame(model.n_inputs, u.pix),
                        output_frame=self.frame)

    @property
    def dropped_world_dimensions(self):
        return self._dropped_world_dimensions


class QuantityTableCoordinate(BaseTableCoordinate):
    """
    A lookup table made up of ``N`` `~astropy.units.Quantity` objects.

    This class can either be instantiated with N ND arrays (i.e. the output of
    `numpy.meshgrid`) or N 1D arrays (i.e. the input to `numpy.meshgrid`).

    Notes
    -----
    The reason for supporting both the input and output of meshgrid is that
    meshgrid isn't called when ``mesh=True``, the "meshing" is done in the gWCS
    layer.
    """
    def __init__(self, *tables, mesh=False, names=None, physical_types=None):
        if not all([isinstance(t, u.Quantity) for t in tables]):
            raise TypeError("All tables must be astropy Quantity objects")
        if not all([t.unit.is_equivalent(tables[0].unit) for t in tables]):
            raise u.UnitsError("All tables must have equivalent units.")

        if isinstance(names, str):
            names = [names]
        if isinstance(physical_types, str):
            physical_types = [physical_types]

        if names is not None and len(names) != len(tables):
            raise ValueError("The number of names should match the number of world dimensions")
        if physical_types is not None and len(physical_types) != len(tables):
            raise ValueError("The number of physical types should match the number of world dimensions")

        self.unit = tables[0].unit

        dims = np.array([t.ndim for t in tables])
        if not mesh and any(dims > 1):
            raise NotImplementedError("Support for lookup tables with more than one dimension is not yet implemented")

        super().__init__(*tables, mesh=mesh, names=names, physical_types=physical_types)

    def _slice_table(self, i, table, item, new_components, whole_slice):
        """
        Apply a slice, or part of a slice to one of the quantity arrays.

        i is the index of the element in `self.table`
        table is the element in `self.table`
        item is the part of the slice to be applied to `table`
        new_components is the dictionary to append the output to
        whole_slice is the complete slice being applied to the whole Table object.
        """
        # If mesh is True then we can drop a dimension
        # If mesh is false then all the dimensions contained in this Table are
        # coupled so we can never drop only one of them only this whole Table
        # can be dropped.
        if isinstance(item, Integral) and (
                isinstance(whole_slice, tuple) and
                not(all(isinstance(k, Integral) for k in whole_slice))):
            dwd = new_components["dropped_world_dimensions"]
            dwd["value"].append(table[item])
            dwd["world_axis_names"].append(self.names[i] if self.names else None)
            dwd["world_axis_physical_types"].append(self.frame.axis_physical_types[i])
            dwd["world_axis_units"].append(table.unit.to_string())
            dwd["world_axis_object_components"].append((f"quantity{i}", 0, "value"))
            dwd["world_axis_object_classes"].update({f"quantity{i}": (u.Quantity, tuple(), {"unit", table.unit.to_string()})})
            return

        new_components["tables"].append(table[item])
        if self.names:
            new_components["names"].append(self.names[i])
        if self.physical_types:
            new_components["physical_types"].append(self.physical_types[i])

    def __getitem__(self, item):
        if isinstance(item, (slice, Integral)):
            item = (item,)
        if not (len(item) == len(self.table) or len(item) == self.table[0].ndim):
            raise ValueError("Can not slice with incorrect length")

        new_components = defaultdict(list)
        new_components["dropped_world_dimensions"] = copy.deepcopy(self._dropped_world_dimensions)

        if self.mesh:
            for i, (ele, table) in enumerate(zip(item, self.table)):
                self._slice_table(i, table, ele, new_components, whole_slice=item)
        else:
            for i, table in enumerate(self.table):
                self._slice_table(i, table, item, new_components, whole_slice=item)

        names = new_components["names"] or None
        physical_types = new_components["physical_types"] or None

        ret_table = type(self)(*new_components["tables"], mesh=self.mesh, names=names, physical_types=physical_types)
        ret_table._dropped_world_dimensions = new_components["dropped_world_dimensions"]
        return ret_table

    @property
    def n_inputs(self):
        return len(self.table)

    def is_scalar(self):
        return all(t.shape == tuple() for t in self.table)

    @property
    def frame(self):
        """
        Generate the Frame for this LookupTable.
        """
        return _generate_generic_frame(len(self.table), self.unit, self.names, self.physical_types)

    @property
    def model(self):
        """
        Generate the Astropy Model for this LookupTable.
        """
        return _model_from_quantity(self.table, self.mesh)


class SkyCoordTableCoordinate(BaseTableCoordinate):
    """
    A lookup table created from a `~astropy.coordinates.SkyCoord`.

    If mesh is `True` in this class then `numpy.meshgrid` *is* called when the
    class is constructed, this is to allow slicing operations on the tables
    which make the length of the dimensions different.
    """
    def __init__(self, *tables, mesh=False, names=None, physical_types=None):
        if not len(tables) == 1 and isinstance(tables[0], SkyCoord):
            raise ValueError("SkyCoordLookupTable can only be constructed from a single SkyCoord object")

        if isinstance(names, str):
            names = [names]
        if names is not None and len(names) != 2:
            raise ValueError("The number of names must equal two for a SkyCoord table.")
        if physical_types is not None and len(physical_types) != 2:
            raise ValueError("The number of physical types must equal two for a SkyCoord table.")

        sc = tables[0]

        super().__init__(sc, mesh=mesh, names=names, physical_types=physical_types)
        self.table = self.table[0]
        self._slice = sanitize_slices(np.s_[...], self.n_inputs)

    @property
    def n_inputs(self):
        return len(self.table.data.components)

    def is_scalar(self):
        return self.table.shape == tuple()

    @staticmethod
    def combine_slices(slice1, slice2):
        ints = [isinstance(s, Integral) for s in (slice1, slice2)]
        if all(ints):
            raise ValueError("Can not combine two integers")
        if any(ints):
            return (slice1, slice2)[ints.index(True)]
        return combine_slices(slice1, slice2)

    def __getitem__(self, item):
        # override the error for consistency
        try:
            sane_item = sanitize_slices(item, self.n_inputs)
        except ValueError as ex:
            raise ValueError("Can not slice with incorrect length") from ex

        if not self.mesh:
            return type(self)(self.table[item],
                              mesh=False,
                              names=self.names,
                              physical_types=self.physical_types)
        else:
            self._slice = [self.combine_slices(a, b) for a, b in zip(sane_item, self._slice)]
            if all([isinstance(s, Integral) for s in self._slice]):
                # Here we rebuild the SkyCoord with the slice applied to the individual components.
                new_sc = SkyCoord(self.table.realize_frame(type(self.table.data)(*self._sliced_components)))
                return type(self)(new_sc,
                                  mesh=False,
                                  names=self.names,
                                  physical_types=self.physical_types)
            return self

    @property
    def frame(self):
        """
        Generate the Frame for this LookupTable.
        """
        sc = self.table
        components = tuple(getattr(sc.data, comp) for comp in sc.data.components)
        ref_frame = sc.frame.replicate_without_data()
        units = list(c.unit for c in components)

        # TODO: Currently this limits you to 2D due to gwcs#120
        return cf.CelestialFrame(reference_frame=ref_frame,
                                 unit=units,
                                 axes_names=self.names,
                                 axis_physical_types=self.physical_types,
                                 name="CelestialFrame")

    @property
    def _sliced_components(self):
        return tuple(getattr(self.table.data, comp)[slc]
                     for comp, slc in zip(self.table.data.components, self._slice))

    @property
    def model(self):
        """
        Generate the Astropy Model for this LookupTable.
        """
        return _model_from_quantity(self._sliced_components, mesh=self.mesh)


class TimeTableCoordinate(BaseTableCoordinate):
    """
    A lookup table based on a `~astropy.time.Time`, will always be one dimensional.
    """
    def __init__(self, *tables, names=None, physical_types=None, reference_time=None):
        if not len(tables) == 1 and isinstance(tables[0], Time):
            raise ValueError("TimeLookupTable can only be constructed from a single Time object.")

        if isinstance(names, str):
            names = [names]
        if isinstance(physical_types, str):
            physical_types = [physical_types]

        if names is not None and len(names) != 1:
            raise ValueError("A Time coordinate can only have one name.")
        if physical_types is not None and len(physical_types) != 1:
            raise ValueError("A Time coordinate can only have one physical type.")

        super().__init__(*tables, mesh=False, names=names, physical_types=physical_types)
        self.table = self.table[0]
        self.reference_time = reference_time or self.table[0]

    def __getitem__(self, item):
        if not (isinstance(item, (slice, Integral)) or len(item) == 1):
            raise ValueError("Can not slice with incorrect length")

        return type(self)(self.table[item],
                          names=self.names,
                          physical_types=self.physical_types,
                          reference_time=self.reference_time)

    @property
    def n_inputs(self):
        return 1  # The time table has to be one dimensional

    def is_scalar(self):
        return self.table.shape == tuple()

    @property
    def frame(self):
        """
        Generate the Frame for this LookupTable.
        """
        return cf.TemporalFrame(self.reference_time,
                                unit=u.s,
                                axes_names=self.names,
                                name="TemporalFrame")

    @property
    def model(self):
        """
        Generate the Astropy Model for this LookupTable.
        """
        time = self.table
        deltas = (time - self.reference_time).to(u.s)

        return _model_from_quantity((deltas,), mesh=False)


class MultipleTableCoordinate(BaseTableCoordinate):
    """
    A Holder for multiple multiple `.BaseTableCoordinate` objects.

    This class allows the generation of a gWCS from many `.BaseTableCoordinate`
    objects.

    Parameters
    ----------
    lookup_tables : `BaseTableCoordinate`
        One or more lookup table coordinate classes to combine into a gWCS
        object.

    Notes
    -----
    The most useful method of constructing a ``LookupTableCoord`` class is to
    combine multiple instances of `.BaseTableCoordinate` with the ``&``
    operator.
    """
    def __init__(self, *table_coordinates):
        if not all(isinstance(lt, BaseTableCoordinate) and
                   not(isinstance(lt, MultipleTableCoordinate)) for lt in table_coordinates):
            raise TypeError("All arguments must be BaseTableCoordinate instances, such as QuantityTableCoordinate, "
                            "and not instances of MultipleTableCoordinate.")
        self._table_coords = list(table_coordinates)
        self._dropped_coords = list()

    def __str__(self):
        classname = self.__class__.__name__
        length = len(classname) + sum(len(str(t)) for t in self._table_coords) + 10
        if length > np.get_printoptions()['linewidth']:
            joiner = ',\n ' + (len(classname) + 8) * ' '
        else:
            joiner = ', '

        return f"{classname}(tables=[{joiner.join([str(t) for t in self._table_coords])}])"

    def __and__(self, other):
        if not isinstance(other, BaseTableCoordinate):
            return NotImplemented

        if isinstance(other, MultipleTableCoordinate):
            others = other._table_coords
        else:
            others = [other]

        return type(self)(*(self._table_coords + others))

    def __rand__(self, other):
        # This method should never be called if the left hand operand is a MultipleTableCoordinate
        if not isinstance(other, BaseTableCoordinate) or isinstance(other, MultipleTableCoordinate):
            return NotImplemented

        return type(self)(*([other] + self._table_coords))

    def __getitem__(self, item):
        if isinstance(item, (slice, Integral)):
            item = (item,)

        if not len(item) == self.n_inputs:
            raise ValueError(
                f"length of the slice ({len(item)}) must match the number of coordinates {self.n_inputs}")

        new_tables = []
        dropped_tables = []
        i = 0
        for table in self._table_coords:
            tslice = item[i:i+table.n_inputs]
            i += table.n_inputs
            new_table = table[tslice]
            if new_table.is_scalar():
                dropped_tables.append(new_table)
            else:
                new_tables.append(new_table)

        new = MultipleTableCoordinate(*new_tables)
        new._dropped_coords = dropped_tables
        return new

    @property
    def n_inputs(self):
        return sum(t.n_inputs for t in self._table_coords)

    def is_scalar(self):
        return False

    @property
    def model(self):
        """
        The combined astropy model for all the lookup tables.
        """
        model = self._table_coords[0].model
        for m2 in self._table_coords[1:]:
            model = model & m2.model
        return model

    @property
    def frame(self):
        """
        The gWCS coordinate frame for all the lookup tables.
        """
        if len(self._table_coords) == 1:
            return self._table_coords[0].frame
        else:
            frames = [t.frame for t in self._table_coords]

            # We now have to set the axes_order of all the frames so that we
            # have one consistent WCS with the correct number of pixel
            # dimensions.
            ind = 0
            for f in frames:
                new_ind = ind + f.naxes
                f._axes_order = tuple(range(ind, new_ind))
                ind = new_ind

            return cf.CompositeFrame(frames)

    @property
    def dropped_world_dimensions(self):
        dropped_world_dimensions = defaultdict(list)
        dropped_world_dimensions["world_axis_object_classes"] = dict()

        # Combine the dicts on the tables with our dict
        for lutc in self._table_coords:
            for key, value in lutc.dropped_world_dimensions.items():
                if key == "world_axis_object_classes":
                    dropped_world_dimensions[key].update(value)
                else:
                    dropped_world_dimensions[key] += value

        dropped_multi_table = MultipleTableCoordinate(*self._dropped_coords)

        dropped_world_dimensions["world_axis_names"] += [name or None for name in dropped_multi_table.frame.axes_names]
        dropped_world_dimensions["world_axis_physical_types"] += list(dropped_multi_table.frame.axis_physical_types)
        dropped_world_dimensions["world_axis_units"] += [u.to_string() for u in dropped_multi_table.frame.unit]
        dropped_world_dimensions["world_axis_object_components"] += dropped_multi_table.frame._world_axis_object_components
        dropped_world_dimensions["world_axis_object_classes"].update(dropped_multi_table.frame._world_axis_object_classes)

        for dropped in self._dropped_coords:
            # If the table is a tuple (QuantityTableCoordinate) then we need to
            # squish the input
            if isinstance(dropped.table, tuple):
                coord = dropped.frame.coordinate_to_quantity(*dropped.table)
            else:
                coord = dropped.frame.coordinate_to_quantity(dropped.table)

            # We want the value in the output dict to be a flat list of values
            # in the order of world_axis_object_components, so if we get a
            # tuple of coordinates out of gWCS then append them to the list, if
            # we only get one quantity out then append to the list.
            if isinstance(coord, tuple):
                dropped_world_dimensions["value"] += list(coord)
            else:
                dropped_world_dimensions["value"].append(coord)

        return dropped_world_dimensions
