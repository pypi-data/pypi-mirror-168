"""_1823.py

PermissibleContinuousAxialLoadResults
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1706
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PERMISSIBLE_CONTINUOUS_AXIAL_LOAD_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'PermissibleContinuousAxialLoadResults')


__docformat__ = 'restructuredtext en'
__all__ = ('PermissibleContinuousAxialLoadResults',)


class PermissibleContinuousAxialLoadResults(_0.APIBase):
    """PermissibleContinuousAxialLoadResults

    This is a mastapy class.
    """

    TYPE = _PERMISSIBLE_CONTINUOUS_AXIAL_LOAD_RESULTS

    def __init__(self, instance_to_wrap: 'PermissibleContinuousAxialLoadResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_axial_load_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AllowableAxialLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableAxialLoadFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def allowable_constant_axial_load_ntn(self) -> 'float':
        """float: 'AllowableConstantAxialLoadNTN' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableConstantAxialLoadNTN

        if temp is None:
            return None

        return temp

    @property
    def allowable_intermittent_axial_load_ntn(self) -> 'float':
        """float: 'AllowableIntermittentAxialLoadNTN' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableIntermittentAxialLoadNTN

        if temp is None:
            return None

        return temp

    @property
    def allowable_momentary_axial_load_ntn(self) -> 'float':
        """float: 'AllowableMomentaryAxialLoadNTN' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableMomentaryAxialLoadNTN

        if temp is None:
            return None

        return temp

    @property
    def axial_load(self) -> 'float':
        """float: 'AxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialLoad

        if temp is None:
            return None

        return temp

    @property
    def calculation_method(self) -> '_1706.CylindricalRollerMaxAxialLoadMethod':
        """CylindricalRollerMaxAxialLoadMethod: 'CalculationMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1706.CylindricalRollerMaxAxialLoadMethod)(value) if value is not None else None

    @property
    def capacity_lubrication_factor_for_permissible_axial_load_grease(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CapacityLubricationFactorForPermissibleAxialLoadGrease' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CapacityLubricationFactorForPermissibleAxialLoadGrease

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def capacity_lubrication_factor_for_permissible_axial_load_oil(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'CapacityLubricationFactorForPermissibleAxialLoadOil' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CapacityLubricationFactorForPermissibleAxialLoadOil

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def diameter_exponent_factor_for_permissible_axial_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DiameterExponentFactorForPermissibleAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterExponentFactorForPermissibleAxialLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def diameter_scaling_factor_for_permissible_axial_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DiameterScalingFactorForPermissibleAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterScalingFactorForPermissibleAxialLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def maximum_permissible_axial_load_schaeffler(self) -> 'float':
        """float: 'MaximumPermissibleAxialLoadSchaeffler' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumPermissibleAxialLoadSchaeffler

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_load_schaeffler(self) -> 'float':
        """float: 'PermissibleAxialLoadSchaeffler' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadSchaeffler

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_load_dimension_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PermissibleAxialLoadDimensionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadDimensionFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def permissible_axial_load_internal_dimension_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PermissibleAxialLoadInternalDimensionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadInternalDimensionFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def permissible_axial_load_under_shaft_deflection_schaeffler(self) -> 'float':
        """float: 'PermissibleAxialLoadUnderShaftDeflectionSchaeffler' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadUnderShaftDeflectionSchaeffler

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_load_for_brief_periods_skf(self) -> 'float':
        """float: 'PermissibleAxialLoadForBriefPeriodsSKF' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadForBriefPeriodsSKF

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_load_for_occasional_peak_loads_skf(self) -> 'float':
        """float: 'PermissibleAxialLoadForOccasionalPeakLoadsSKF' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadForOccasionalPeakLoadsSKF

        if temp is None:
            return None

        return temp

    @property
    def permissible_axial_loading_nachi(self) -> 'float':
        """float: 'PermissibleAxialLoadingNACHI' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleAxialLoadingNACHI

        if temp is None:
            return None

        return temp

    @property
    def permissible_continuous_axial_load_skf(self) -> 'float':
        """float: 'PermissibleContinuousAxialLoadSKF' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PermissibleContinuousAxialLoadSKF

        if temp is None:
            return None

        return temp

    @property
    def radial_load_lubrication_factor_for_permissible_axial_load_grease(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadialLoadLubricationFactorForPermissibleAxialLoadGrease' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialLoadLubricationFactorForPermissibleAxialLoadGrease

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def radial_load_lubrication_factor_for_permissible_axial_load_oil(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RadialLoadLubricationFactorForPermissibleAxialLoadOil' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialLoadLubricationFactorForPermissibleAxialLoadOil

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def safety_factor(self) -> 'float':
        """float: 'SafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactor

        if temp is None:
            return None

        return temp
