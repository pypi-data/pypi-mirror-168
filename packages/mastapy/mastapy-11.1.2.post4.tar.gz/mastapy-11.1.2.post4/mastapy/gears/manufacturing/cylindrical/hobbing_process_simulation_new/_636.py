"""_636.py

HobbingProcessPitchCalculation
"""


from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _627, _632
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_PITCH_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessPitchCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessPitchCalculation',)


class HobbingProcessPitchCalculation(_632.HobbingProcessCalculation):
    """HobbingProcessPitchCalculation

    This is a mastapy class.
    """

    TYPE = _HOBBING_PROCESS_PITCH_CALCULATION

    def __init__(self, instance_to_wrap: 'HobbingProcessPitchCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def pitch_modification_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'PitchModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchModificationChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast pitch_modification_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def result_z_plane(self) -> 'float':
        """float: 'ResultZPlane' is the original name of this property."""

        temp = self.wrapped.ResultZPlane

        if temp is None:
            return None

        return temp

    @result_z_plane.setter
    def result_z_plane(self, value: 'float'):
        self.wrapped.ResultZPlane = float(value) if value else 0.0

    @property
    def left_flank(self) -> '_627.CalculatePitchDeviationAccuracy':
        """CalculatePitchDeviationAccuracy: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_627.CalculatePitchDeviationAccuracy':
        """CalculatePitchDeviationAccuracy: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
