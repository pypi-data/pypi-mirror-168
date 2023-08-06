"""_921.py

WormGearMeshDesign
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.worm import (
    _923, _919, _922, _920
)
from mastapy.gears.gear_designs import _912
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Worm', 'WormGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshDesign',)


class WormGearMeshDesign(_912.GearMeshDesign):
    """WormGearMeshDesign

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_DESIGN

    def __init__(self, instance_to_wrap: 'WormGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property."""

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def coefficient_of_friction(self) -> 'float':
        """float: 'CoefficientOfFriction' is the original name of this property."""

        temp = self.wrapped.CoefficientOfFriction

        if temp is None:
            return None

        return temp

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'float'):
        self.wrapped.CoefficientOfFriction = float(value) if value else 0.0

    @property
    def meshing_friction_angle(self) -> 'float':
        """float: 'MeshingFrictionAngle' is the original name of this property."""

        temp = self.wrapped.MeshingFrictionAngle

        if temp is None:
            return None

        return temp

    @meshing_friction_angle.setter
    def meshing_friction_angle(self, value: 'float'):
        self.wrapped.MeshingFrictionAngle = float(value) if value else 0.0

    @property
    def shaft_angle(self) -> 'float':
        """float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return temp

    @property
    def standard_centre_distance(self) -> 'float':
        """float: 'StandardCentreDistance' is the original name of this property."""

        temp = self.wrapped.StandardCentreDistance

        if temp is None:
            return None

        return temp

    @standard_centre_distance.setter
    def standard_centre_distance(self, value: 'float'):
        self.wrapped.StandardCentreDistance = float(value) if value else 0.0

    @property
    def wheel_addendum_modification_factor(self) -> 'float':
        """float: 'WheelAddendumModificationFactor' is the original name of this property."""

        temp = self.wrapped.WheelAddendumModificationFactor

        if temp is None:
            return None

        return temp

    @wheel_addendum_modification_factor.setter
    def wheel_addendum_modification_factor(self, value: 'float'):
        self.wrapped.WheelAddendumModificationFactor = float(value) if value else 0.0

    @property
    def wheel(self) -> '_923.WormWheelDesign':
        """WormWheelDesign: 'Wheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Wheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm(self) -> '_919.WormDesign':
        """WormDesign: 'Worm' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Worm

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_set(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'WormGearSet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSet

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gears(self) -> 'List[_920.WormGearDesign]':
        """List[WormGearDesign]: 'WormGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
