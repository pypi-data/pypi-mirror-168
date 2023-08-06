"""_634.py

HobbingProcessLeadCalculation
"""


from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _626, _632
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_LEAD_CALCULATION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessLeadCalculation')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessLeadCalculation',)


class HobbingProcessLeadCalculation(_632.HobbingProcessCalculation):
    """HobbingProcessLeadCalculation

    This is a mastapy class.
    """

    TYPE = _HOBBING_PROCESS_LEAD_CALCULATION

    def __init__(self, instance_to_wrap: 'HobbingProcessLeadCalculation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def left_flank_lead_modification_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'LeftFlankLeadModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlankLeadModificationChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast left_flank_lead_modification_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def number_of_lead_bands(self) -> 'int':
        """int: 'NumberOfLeadBands' is the original name of this property."""

        temp = self.wrapped.NumberOfLeadBands

        if temp is None:
            return None

        return temp

    @number_of_lead_bands.setter
    def number_of_lead_bands(self, value: 'int'):
        self.wrapped.NumberOfLeadBands = int(value) if value else 0

    @property
    def radius_for_lead_modification_calculation(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadiusForLeadModificationCalculation' is the original name of this property."""

        temp = self.wrapped.RadiusForLeadModificationCalculation

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @radius_for_lead_modification_calculation.setter
    def radius_for_lead_modification_calculation(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RadiusForLeadModificationCalculation = value

    @property
    def right_flank_lead_modification_chart(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'RightFlankLeadModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlankLeadModificationChart

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast right_flank_lead_modification_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank(self) -> '_626.CalculateLeadDeviationAccuracy':
        """CalculateLeadDeviationAccuracy: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_626.CalculateLeadDeviationAccuracy':
        """CalculateLeadDeviationAccuracy: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
