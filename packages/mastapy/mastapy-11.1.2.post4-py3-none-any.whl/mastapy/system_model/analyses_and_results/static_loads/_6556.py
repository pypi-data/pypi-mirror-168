"""_6556.py

ClutchConnectionLoadCase
"""


from mastapy._internal import constructor
from mastapy.math_utility import _1341
from mastapy.system_model.connections_and_sockets.couplings import _2093
from mastapy.system_model.analyses_and_results.static_loads import _6574
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ClutchConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionLoadCase',)


class ClutchConnectionLoadCase(_6574.CouplingConnectionLoadCase):
    """ClutchConnectionLoadCase

    This is a mastapy class.
    """

    TYPE = _CLUTCH_CONNECTION_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ClutchConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_initial_temperature(self) -> 'float':
        """float: 'ClutchInitialTemperature' is the original name of this property."""

        temp = self.wrapped.ClutchInitialTemperature

        if temp is None:
            return None

        return temp

    @clutch_initial_temperature.setter
    def clutch_initial_temperature(self, value: 'float'):
        self.wrapped.ClutchInitialTemperature = float(value) if value else 0.0

    @property
    def clutch_pressures(self) -> '_1341.Vector2DListAccessor':
        """Vector2DListAccessor: 'ClutchPressures' is the original name of this property."""

        temp = self.wrapped.ClutchPressures

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @clutch_pressures.setter
    def clutch_pressures(self, value: '_1341.Vector2DListAccessor'):
        value = value.wrapped if value else None
        self.wrapped.ClutchPressures = value

    @property
    def is_initially_locked(self) -> 'bool':
        """bool: 'IsInitiallyLocked' is the original name of this property."""

        temp = self.wrapped.IsInitiallyLocked

        if temp is None:
            return None

        return temp

    @is_initially_locked.setter
    def is_initially_locked(self, value: 'bool'):
        self.wrapped.IsInitiallyLocked = bool(value) if value else False

    @property
    def unlocked_clutch_linear_resistance_coefficient(self) -> 'float':
        """float: 'UnlockedClutchLinearResistanceCoefficient' is the original name of this property."""

        temp = self.wrapped.UnlockedClutchLinearResistanceCoefficient

        if temp is None:
            return None

        return temp

    @unlocked_clutch_linear_resistance_coefficient.setter
    def unlocked_clutch_linear_resistance_coefficient(self, value: 'float'):
        self.wrapped.UnlockedClutchLinearResistanceCoefficient = float(value) if value else 0.0

    @property
    def use_fixed_update_time(self) -> 'bool':
        """bool: 'UseFixedUpdateTime' is the original name of this property."""

        temp = self.wrapped.UseFixedUpdateTime

        if temp is None:
            return None

        return temp

    @use_fixed_update_time.setter
    def use_fixed_update_time(self, value: 'bool'):
        self.wrapped.UseFixedUpdateTime = bool(value) if value else False

    @property
    def connection_design(self) -> '_2093.ClutchConnection':
        """ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
