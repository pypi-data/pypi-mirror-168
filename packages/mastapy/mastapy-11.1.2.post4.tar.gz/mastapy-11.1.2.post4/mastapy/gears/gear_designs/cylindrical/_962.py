"""_962.py

BacklashSpecification
"""


from typing import List

from mastapy.gears.gear_designs.cylindrical import _1019, _997, _1029
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_BACKLASH_SPECIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'BacklashSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('BacklashSpecification',)


class BacklashSpecification(_1029.RelativeValuesSpecification['BacklashSpecification']):
    """BacklashSpecification

    This is a mastapy class.
    """

    TYPE = _BACKLASH_SPECIFICATION

    def __init__(self, instance_to_wrap: 'BacklashSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def left_flank(self) -> '_1019.LinearBacklashSepcification':
        """LinearBacklashSepcification: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_1019.LinearBacklashSepcification':
        """LinearBacklashSepcification: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def angular_backlash(self) -> 'List[_997.CylindricalMeshAngularBacklash]':
        """List[CylindricalMeshAngularBacklash]: 'AngularBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularBacklash

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flanks(self) -> 'List[_1019.LinearBacklashSepcification]':
        """List[LinearBacklashSepcification]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Flanks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def both_flanks(self) -> '_1019.LinearBacklashSepcification':
        """LinearBacklashSepcification: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BothFlanks

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
