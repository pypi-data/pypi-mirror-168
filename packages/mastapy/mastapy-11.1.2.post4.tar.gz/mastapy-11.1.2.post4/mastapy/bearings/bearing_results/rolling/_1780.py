"""_1780.py

LoadedNeedleRollerBearingRow
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1779, _1768
from mastapy._internal.python_net import python_net_import

_LOADED_NEEDLE_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedNeedleRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNeedleRollerBearingRow',)


class LoadedNeedleRollerBearingRow(_1768.LoadedCylindricalRollerBearingRow):
    """LoadedNeedleRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_NEEDLE_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedNeedleRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cage_land_sliding_power_loss(self) -> 'float':
        """float: 'CageLandSlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CageLandSlidingPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def rolling_power_loss(self) -> 'float':
        """float: 'RollingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def rolling_power_loss_traction_coefficient(self) -> 'float':
        """float: 'RollingPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingPowerLossTractionCoefficient

        if temp is None:
            return None

        return temp

    @property
    def sliding_power_loss(self) -> 'float':
        """float: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def sliding_power_loss_traction_coefficient(self) -> 'float':
        """float: 'SlidingPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingPowerLossTractionCoefficient

        if temp is None:
            return None

        return temp

    @property
    def total_power_loss(self) -> 'float':
        """float: 'TotalPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def total_power_loss_traction_coefficient(self) -> 'float':
        """float: 'TotalPowerLossTractionCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalPowerLossTractionCoefficient

        if temp is None:
            return None

        return temp

    @property
    def loaded_bearing(self) -> '_1779.LoadedNeedleRollerBearingResults':
        """LoadedNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
