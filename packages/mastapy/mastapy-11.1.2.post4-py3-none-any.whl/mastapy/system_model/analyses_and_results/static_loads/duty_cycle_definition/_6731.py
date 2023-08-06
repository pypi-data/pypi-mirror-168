"""_6731.py

TorqueInputOptions
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6732, _6726
from mastapy._internal.python_net import python_net_import

_TORQUE_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'TorqueInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueInputOptions',)


class TorqueInputOptions(_6726.PowerLoadInputOptions):
    """TorqueInputOptions

    This is a mastapy class.
    """

    TYPE = _TORQUE_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'TorqueInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bin_start(self) -> 'float':
        """float: 'BinStart' is the original name of this property."""

        temp = self.wrapped.BinStart

        if temp is None:
            return None

        return temp

    @bin_start.setter
    def bin_start(self, value: 'float'):
        self.wrapped.BinStart = float(value) if value else 0.0

    @property
    def bin_width(self) -> 'float':
        """float: 'BinWidth' is the original name of this property."""

        temp = self.wrapped.BinWidth

        if temp is None:
            return None

        return temp

    @bin_width.setter
    def bin_width(self, value: 'float'):
        self.wrapped.BinWidth = float(value) if value else 0.0

    @property
    def conversion_to_load_case(self) -> '_6732.TorqueValuesObtainedFrom':
        """TorqueValuesObtainedFrom: 'ConversionToLoadCase' is the original name of this property."""

        temp = self.wrapped.ConversionToLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6732.TorqueValuesObtainedFrom)(value) if value is not None else None

    @conversion_to_load_case.setter
    def conversion_to_load_case(self, value: '_6732.TorqueValuesObtainedFrom'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConversionToLoadCase = value

    @property
    def include_bin_boundary_at_zero(self) -> 'bool':
        """bool: 'IncludeBinBoundaryAtZero' is the original name of this property."""

        temp = self.wrapped.IncludeBinBoundaryAtZero

        if temp is None:
            return None

        return temp

    @include_bin_boundary_at_zero.setter
    def include_bin_boundary_at_zero(self, value: 'bool'):
        self.wrapped.IncludeBinBoundaryAtZero = bool(value) if value else False

    @property
    def number_of_bins(self) -> 'int':
        """int: 'NumberOfBins' is the original name of this property."""

        temp = self.wrapped.NumberOfBins

        if temp is None:
            return None

        return temp

    @number_of_bins.setter
    def number_of_bins(self, value: 'int'):
        self.wrapped.NumberOfBins = int(value) if value else 0

    @property
    def specify_bins(self) -> 'bool':
        """bool: 'SpecifyBins' is the original name of this property."""

        temp = self.wrapped.SpecifyBins

        if temp is None:
            return None

        return temp

    @specify_bins.setter
    def specify_bins(self, value: 'bool'):
        self.wrapped.SpecifyBins = bool(value) if value else False
