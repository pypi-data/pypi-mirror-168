"""_358.py

KlingelnbergVirtualCylindricalGear
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import _360
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'KlingelnbergVirtualCylindricalGear')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergVirtualCylindricalGear',)


class KlingelnbergVirtualCylindricalGear(_360.VirtualCylindricalGear):
    """KlingelnbergVirtualCylindricalGear

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_VIRTUAL_CYLINDRICAL_GEAR

    def __init__(self, instance_to_wrap: 'KlingelnbergVirtualCylindricalGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_face_width(self) -> 'float':
        """float: 'EffectiveFaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveFaceWidth

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
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def outside_diameter_of_virtual_cylindrical_gear(self) -> 'float':
        """float: 'OutsideDiameterOfVirtualCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OutsideDiameterOfVirtualCylindricalGear

        if temp is None:
            return None

        return temp

    @property
    def virtual_number_of_teeth_normal(self) -> 'float':
        """float: 'VirtualNumberOfTeethNormal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualNumberOfTeethNormal

        if temp is None:
            return None

        return temp

    @property
    def virtual_number_of_teeth_transverse(self) -> 'float':
        """float: 'VirtualNumberOfTeethTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualNumberOfTeethTransverse

        if temp is None:
            return None

        return temp
