"""_1019.py

LinearBacklashSepcification
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _1000, _997
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LINEAR_BACKLASH_SEPCIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'LinearBacklashSepcification')


__docformat__ = 'restructuredtext en'
__all__ = ('LinearBacklashSepcification',)


class LinearBacklashSepcification(_0.APIBase):
    """LinearBacklashSepcification

    This is a mastapy class.
    """

    TYPE = _LINEAR_BACKLASH_SEPCIFICATION

    def __init__(self, instance_to_wrap: 'LinearBacklashSepcification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def flank_name(self) -> 'str':
        """str: 'FlankName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlankName

        if temp is None:
            return None

        return temp

    @property
    def circumferential_backlash_pitch_circle(self) -> '_1000.CylindricalMeshLinearBacklashSpecification':
        """CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashPitchCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CircumferentialBacklashPitchCircle

        if temp is None:
            return None

        if _1000.CylindricalMeshLinearBacklashSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast circumferential_backlash_pitch_circle to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def circumferential_backlash_reference_circle(self) -> '_1000.CylindricalMeshLinearBacklashSpecification':
        """CylindricalMeshLinearBacklashSpecification: 'CircumferentialBacklashReferenceCircle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CircumferentialBacklashReferenceCircle

        if temp is None:
            return None

        if _1000.CylindricalMeshLinearBacklashSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast circumferential_backlash_reference_circle to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def normal_backlash(self) -> '_1000.CylindricalMeshLinearBacklashSpecification':
        """CylindricalMeshLinearBacklashSpecification: 'NormalBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalBacklash

        if temp is None:
            return None

        if _1000.CylindricalMeshLinearBacklashSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast normal_backlash to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def radial_backlash(self) -> '_1000.CylindricalMeshLinearBacklashSpecification':
        """CylindricalMeshLinearBacklashSpecification: 'RadialBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialBacklash

        if temp is None:
            return None

        if _1000.CylindricalMeshLinearBacklashSpecification.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast radial_backlash to CylindricalMeshLinearBacklashSpecification. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_backlash(self) -> 'List[_1000.CylindricalMeshLinearBacklashSpecification]':
        """List[CylindricalMeshLinearBacklashSpecification]: 'LinearBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearBacklash

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
