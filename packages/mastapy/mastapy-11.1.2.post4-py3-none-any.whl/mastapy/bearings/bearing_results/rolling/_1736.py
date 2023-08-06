"""_1736.py

ISO14179Settings
"""


from mastapy.bearings.bearing_results.rolling import _1824
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.math_utility.measured_data import _1375, _1376
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_ISO14179_SETTINGS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'ISO14179Settings')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO14179Settings',)


class ISO14179Settings(_1605.NamedDatabaseItem):
    """ISO14179Settings

    This is a mastapy class.
    """

    TYPE = _ISO14179_SETTINGS

    def __init__(self, instance_to_wrap: 'ISO14179Settings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def isotr141792001f1_specification_method(self) -> '_1824.PowerRatingF1EstimationMethod':
        """PowerRatingF1EstimationMethod: 'ISOTR141792001F1SpecificationMethod' is the original name of this property."""

        temp = self.wrapped.ISOTR141792001F1SpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1824.PowerRatingF1EstimationMethod)(value) if value is not None else None

    @isotr141792001f1_specification_method.setter
    def isotr141792001f1_specification_method(self, value: '_1824.PowerRatingF1EstimationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISOTR141792001F1SpecificationMethod = value

    @property
    def user_specified_f1_for_isotr141792001(self) -> 'float':
        """float: 'UserSpecifiedF1ForISOTR141792001' is the original name of this property."""

        temp = self.wrapped.UserSpecifiedF1ForISOTR141792001

        if temp is None:
            return None

        return temp

    @user_specified_f1_for_isotr141792001.setter
    def user_specified_f1_for_isotr141792001(self, value: 'float'):
        self.wrapped.UserSpecifiedF1ForISOTR141792001 = float(value) if value else 0.0

    @property
    def power_rating_f0_scaling_factor_one_dimensional_lookup_table(self) -> '_1375.OnedimensionalFunctionLookupTable':
        """OnedimensionalFunctionLookupTable: 'PowerRatingF0ScalingFactorOneDimensionalLookupTable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF0ScalingFactorOneDimensionalLookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_rating_f1_one_dimensional_lookup_table(self) -> '_1375.OnedimensionalFunctionLookupTable':
        """OnedimensionalFunctionLookupTable: 'PowerRatingF1OneDimensionalLookupTable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF1OneDimensionalLookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_rating_f1_scaling_factor_one_dimensional_lookup_table(self) -> '_1375.OnedimensionalFunctionLookupTable':
        """OnedimensionalFunctionLookupTable: 'PowerRatingF1ScalingFactorOneDimensionalLookupTable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF1ScalingFactorOneDimensionalLookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_rating_f1_two_dimensional_lookup_table(self) -> '_1376.TwodimensionalFunctionLookupTable':
        """TwodimensionalFunctionLookupTable: 'PowerRatingF1TwoDimensionalLookupTable' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerRatingF1TwoDimensionalLookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
