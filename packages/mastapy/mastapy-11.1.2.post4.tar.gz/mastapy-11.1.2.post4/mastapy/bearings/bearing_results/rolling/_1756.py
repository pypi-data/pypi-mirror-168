"""_1756.py

LoadedAxialThrustNeedleRollerBearingRow
"""


from mastapy.bearings.bearing_results.rolling import _1755, _1753
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedAxialThrustNeedleRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedAxialThrustNeedleRollerBearingRow',)


class LoadedAxialThrustNeedleRollerBearingRow(_1753.LoadedAxialThrustCylindricalRollerBearingRow):
    """LoadedAxialThrustNeedleRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_AXIAL_THRUST_NEEDLE_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedAxialThrustNeedleRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def loaded_bearing(self) -> '_1755.LoadedAxialThrustNeedleRollerBearingResults':
        """LoadedAxialThrustNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
