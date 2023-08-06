"""_1768.py

LoadedCylindricalRollerBearingRow
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import _1767, _1779, _1783
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_CYLINDRICAL_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedCylindricalRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedCylindricalRollerBearingRow',)


class LoadedCylindricalRollerBearingRow(_1783.LoadedNonBarrelRollerBearingRow):
    """LoadedCylindricalRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_CYLINDRICAL_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedCylindricalRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rib_normal_contact_stress_inner_left(self) -> 'Image':
        """Image: 'RibNormalContactStressInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RibNormalContactStressInnerLeft

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def rib_normal_contact_stress_inner_right(self) -> 'Image':
        """Image: 'RibNormalContactStressInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RibNormalContactStressInnerRight

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def rib_normal_contact_stress_outer_left(self) -> 'Image':
        """Image: 'RibNormalContactStressOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RibNormalContactStressOuterLeft

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def rib_normal_contact_stress_outer_right(self) -> 'Image':
        """Image: 'RibNormalContactStressOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RibNormalContactStressOuterRight

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def loaded_bearing(self) -> '_1767.LoadedCylindricalRollerBearingResults':
        """LoadedCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1767.LoadedCylindricalRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCylindricalRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
