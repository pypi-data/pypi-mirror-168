"""_364.py

VirtualCylindricalGearSet
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.gears.rating.virtual_cylindrical_gears import _361
from mastapy._internal.python_net import python_net_import

_VIRTUAL_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'VirtualCylindricalGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualCylindricalGearSet',)


T = TypeVar('T', bound='_361.VirtualCylindricalGearBasic')


class VirtualCylindricalGearSet(_0.APIBase, Generic[T]):
    """VirtualCylindricalGearSet

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _VIRTUAL_CYLINDRICAL_GEAR_SET

    def __init__(self, instance_to_wrap: 'VirtualCylindricalGearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_face_width_of_virtual_cylindrical_gears(self) -> 'float':
        """float: 'EffectiveFaceWidthOfVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidthOfVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def face_contact_ratio_transverse_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'FaceContactRatioTransverseForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceContactRatioTransverseForVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def face_width_of_virtual_cylindrical_gears(self) -> 'float':
        """float: 'FaceWidthOfVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidthOfVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio_normal_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'TransverseContactRatioNormalForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatioNormalForVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def transverse_contact_ratio_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'TransverseContactRatioForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseContactRatioForVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def virtual_centre_distance(self) -> 'float':
        """float: 'VirtualCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCentreDistance

        if temp is None:
            return None

        return temp

    @property
    def virtual_contact_ratio_transverse_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'VirtualContactRatioTransverseForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualContactRatioTransverseForVirtualCylindricalGears

        if temp is None:
            return None

        return temp

    @property
    def virtual_pinion(self) -> 'T':
        """T: 'VirtualPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualPinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_wheel(self) -> 'T':
        """T: 'VirtualWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_cylindrical_gears(self) -> 'List[T]':
        """List[T]: 'VirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
