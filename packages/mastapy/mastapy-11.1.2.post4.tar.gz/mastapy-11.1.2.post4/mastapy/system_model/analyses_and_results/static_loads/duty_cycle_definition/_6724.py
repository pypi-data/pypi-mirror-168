"""_6724.py

MultiTimeSeriesDataInputFileOptions
"""


from mastapy._internal import constructor
from mastapy.utility.file_access_helpers import _1595
from mastapy.utility_gui import _1623
from mastapy._internal.python_net import python_net_import

_MULTI_TIME_SERIES_DATA_INPUT_FILE_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'MultiTimeSeriesDataInputFileOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('MultiTimeSeriesDataInputFileOptions',)


class MultiTimeSeriesDataInputFileOptions(_1623.DataInputFileOptions):
    """MultiTimeSeriesDataInputFileOptions

    This is a mastapy class.
    """

    TYPE = _MULTI_TIME_SERIES_DATA_INPUT_FILE_OPTIONS

    def __init__(self, instance_to_wrap: 'MultiTimeSeriesDataInputFileOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duration(self) -> 'float':
        """float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Duration

        if temp is None:
            return None

        return temp

    @property
    def duration_scaling(self) -> 'float':
        """float: 'DurationScaling' is the original name of this property."""

        temp = self.wrapped.DurationScaling

        if temp is None:
            return None

        return temp

    @duration_scaling.setter
    def duration_scaling(self, value: 'float'):
        self.wrapped.DurationScaling = float(value) if value else 0.0

    @property
    def proportion_of_duty_cycle(self) -> 'float':
        """float: 'ProportionOfDutyCycle' is the original name of this property."""

        temp = self.wrapped.ProportionOfDutyCycle

        if temp is None:
            return None

        return temp

    @proportion_of_duty_cycle.setter
    def proportion_of_duty_cycle(self, value: 'float'):
        self.wrapped.ProportionOfDutyCycle = float(value) if value else 0.0

    @property
    def delimiter_options(self) -> '_1595.TextFileDelimiterOptions':
        """TextFileDelimiterOptions: 'DelimiterOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DelimiterOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
