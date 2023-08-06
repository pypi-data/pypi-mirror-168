"""_2318.py

CycloidalDisc
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import
from mastapy.cycloidal import _1262, _1263, _1269
from mastapy.materials import _245, _223
from mastapy.shafts import _24
from mastapy._internal.cast_exception import CastException
from mastapy.gears.materials import (
    _549, _551, _553, _557,
    _560, _563, _567, _569
)
from mastapy.detailed_rigid_connectors.splines import _1224
from mastapy.bolts import _1272, _1276
from mastapy.system_model.part_model import _2211, _2187
from mastapy.system_model.connections_and_sockets.cycloidal import _2090

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDisc',)


class CycloidalDisc(_2187.AbstractShaft):
    """CycloidalDisc

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC

    def __init__(self, instance_to_wrap: 'CycloidalDisc.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bore_diameter(self) -> 'float':
        """float: 'BoreDiameter' is the original name of this property."""

        temp = self.wrapped.BoreDiameter

        if temp is None:
            return None

        return temp

    @bore_diameter.setter
    def bore_diameter(self, value: 'float'):
        self.wrapped.BoreDiameter = float(value) if value else 0.0

    @property
    def disc_material_database(self) -> 'str':
        """str: 'DiscMaterialDatabase' is the original name of this property."""

        temp = self.wrapped.DiscMaterialDatabase.SelectedItemName

        if temp is None:
            return None

        return temp

    @disc_material_database.setter
    def disc_material_database(self, value: 'str'):
        self.wrapped.DiscMaterialDatabase.SetSelectedItem(str(value) if value else '')

    @property
    def hole_diameter_for_eccentric_bearing(self) -> 'float':
        """float: 'HoleDiameterForEccentricBearing' is the original name of this property."""

        temp = self.wrapped.HoleDiameterForEccentricBearing

        if temp is None:
            return None

        return temp

    @hole_diameter_for_eccentric_bearing.setter
    def hole_diameter_for_eccentric_bearing(self, value: 'float'):
        self.wrapped.HoleDiameterForEccentricBearing = float(value) if value else 0.0

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return None

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value else 0.0

    @property
    def number_of_planetary_sockets(self) -> 'int':
        """int: 'NumberOfPlanetarySockets' is the original name of this property."""

        temp = self.wrapped.NumberOfPlanetarySockets

        if temp is None:
            return None

        return temp

    @number_of_planetary_sockets.setter
    def number_of_planetary_sockets(self, value: 'int'):
        self.wrapped.NumberOfPlanetarySockets = int(value) if value else 0

    @property
    def cycloidal_disc_design(self) -> '_1262.CycloidalDiscDesign':
        """CycloidalDiscDesign: 'CycloidalDiscDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def disc_material(self) -> '_245.Material':
        """Material: 'DiscMaterial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiscMaterial

        if temp is None:
            return None

        if _245.Material.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast disc_material to Material. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def load_sharing_settings(self) -> '_2211.LoadSharingSettings':
        """LoadSharingSettings: 'LoadSharingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetary_bearing_sockets(self) -> 'List[_2090.CycloidalDiscPlanetaryBearingSocket]':
        """List[CycloidalDiscPlanetaryBearingSocket]: 'PlanetaryBearingSockets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetaryBearingSockets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
