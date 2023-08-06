"""_958.py

FaceGearSetDesign
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.face import (
    _959, _960, _957, _952,
    _954
)
from mastapy.gears.gear_designs import _913
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetDesign',)


class FaceGearSetDesign(_913.GearSetDesign):
    """FaceGearSetDesign

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'FaceGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def module(self) -> 'float':
        """float: 'Module' is the original name of this property."""

        temp = self.wrapped.Module

        if temp is None:
            return None

        return temp

    @module.setter
    def module(self, value: 'float'):
        self.wrapped.Module = float(value) if value else 0.0

    @property
    def nominal_pressure_angle(self) -> 'float':
        """float: 'NominalPressureAngle' is the original name of this property."""

        temp = self.wrapped.NominalPressureAngle

        if temp is None:
            return None

        return temp

    @nominal_pressure_angle.setter
    def nominal_pressure_angle(self, value: 'float'):
        self.wrapped.NominalPressureAngle = float(value) if value else 0.0

    @property
    def normal_base_pitch(self) -> 'float':
        """float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalBasePitch

        if temp is None:
            return None

        return temp

    @property
    def shaft_angle(self) -> 'float':
        """float: 'ShaftAngle' is the original name of this property."""

        temp = self.wrapped.ShaftAngle

        if temp is None:
            return None

        return temp

    @shaft_angle.setter
    def shaft_angle(self, value: 'float'):
        self.wrapped.ShaftAngle = float(value) if value else 0.0

    @property
    def working_normal_pressure_angle(self) -> 'float':
        """float: 'WorkingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingNormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_959.FaceGearSetMicroGeometry':
        """FaceGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSetMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gear(self) -> '_960.FaceGearWheelDesign':
        """FaceGearWheelDesign: 'FaceGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGear

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def pinion(self) -> '_957.FaceGearPinionDesign':
        """FaceGearPinionDesign: 'Pinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Pinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_952.FaceGearDesign]':
        """List[FaceGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gears(self) -> 'List[_952.FaceGearDesign]':
        """List[FaceGearDesign]: 'FaceGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_meshes(self) -> 'List[_954.FaceGearMeshDesign]':
        """List[FaceGearMeshDesign]: 'FaceMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
