"""_1788.py

LoadedRollerBearingRow
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import (
    _1787, _1747, _1752, _1755,
    _1763, _1767, _1779, _1782,
    _1798, _1801, _1807, _1816,
    _1732, _1792
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_LOADED_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedRollerBearingRow',)


class LoadedRollerBearingRow(_1792.LoadedRollingBearingRow):
    """LoadedRollerBearingRow

    This is a mastapy class.
    """

    TYPE = _LOADED_ROLLER_BEARING_ROW

    def __init__(self, instance_to_wrap: 'LoadedRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def depth_of_maximum_shear_stress_chart_inner(self) -> 'Image':
        """Image: 'DepthOfMaximumShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaximumShearStressChartInner

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def depth_of_maximum_shear_stress_chart_outer(self) -> 'Image':
        """Image: 'DepthOfMaximumShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaximumShearStressChartOuter

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def hertzian_contact_width_inner(self) -> 'float':
        """float: 'HertzianContactWidthInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactWidthInner

        if temp is None:
            return None

        return temp

    @property
    def hertzian_contact_width_outer(self) -> 'float':
        """float: 'HertzianContactWidthOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactWidthOuter

        if temp is None:
            return None

        return temp

    @property
    def inner_race_profile_warning(self) -> 'str':
        """str: 'InnerRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerRaceProfileWarning

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_edge_stress_inner(self) -> 'float':
        """float: 'MaximumNormalEdgeStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalEdgeStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_edge_stress_outer(self) -> 'float':
        """float: 'MaximumNormalEdgeStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalEdgeStressOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        """float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        """float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressOuter

        if temp is None:
            return None

        return temp

    @property
    def outer_race_profile_warning(self) -> 'str':
        """str: 'OuterRaceProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRaceProfileWarning

        if temp is None:
            return None

        return temp

    @property
    def roller_profile_warning(self) -> 'str':
        """str: 'RollerProfileWarning' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollerProfileWarning

        if temp is None:
            return None

        return temp

    @property
    def shear_stress_chart_inner(self) -> 'Image':
        """Image: 'ShearStressChartInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearStressChartInner

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def shear_stress_chart_outer(self) -> 'Image':
        """Image: 'ShearStressChartOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearStressChartOuter

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def loaded_bearing(self) -> '_1787.LoadedRollerBearingResults':
        """LoadedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1787.LoadedRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_asymmetric_spherical_roller_bearing_results(self) -> '_1747.LoadedAsymmetricSphericalRollerBearingResults':
        """LoadedAsymmetricSphericalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1747.LoadedAsymmetricSphericalRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAsymmetricSphericalRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_cylindrical_roller_bearing_results(self) -> '_1752.LoadedAxialThrustCylindricalRollerBearingResults':
        """LoadedAxialThrustCylindricalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1752.LoadedAxialThrustCylindricalRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustCylindricalRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_axial_thrust_needle_roller_bearing_results(self) -> '_1755.LoadedAxialThrustNeedleRollerBearingResults':
        """LoadedAxialThrustNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1755.LoadedAxialThrustNeedleRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedAxialThrustNeedleRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_crossed_roller_bearing_results(self) -> '_1763.LoadedCrossedRollerBearingResults':
        """LoadedCrossedRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1763.LoadedCrossedRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedCrossedRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_cylindrical_roller_bearing_results(self) -> '_1767.LoadedCylindricalRollerBearingResults':
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

    @property
    def loaded_bearing_of_type_loaded_needle_roller_bearing_results(self) -> '_1779.LoadedNeedleRollerBearingResults':
        """LoadedNeedleRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1779.LoadedNeedleRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNeedleRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_non_barrel_roller_bearing_results(self) -> '_1782.LoadedNonBarrelRollerBearingResults':
        """LoadedNonBarrelRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1782.LoadedNonBarrelRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedNonBarrelRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_radial_bearing_results(self) -> '_1798.LoadedSphericalRollerRadialBearingResults':
        """LoadedSphericalRollerRadialBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1798.LoadedSphericalRollerRadialBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerRadialBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_spherical_roller_thrust_bearing_results(self) -> '_1801.LoadedSphericalRollerThrustBearingResults':
        """LoadedSphericalRollerThrustBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1801.LoadedSphericalRollerThrustBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedSphericalRollerThrustBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_taper_roller_bearing_results(self) -> '_1807.LoadedTaperRollerBearingResults':
        """LoadedTaperRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1807.LoadedTaperRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedTaperRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def loaded_bearing_of_type_loaded_toroidal_roller_bearing_results(self) -> '_1816.LoadedToroidalRollerBearingResults':
        """LoadedToroidalRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedBearing

        if temp is None:
            return None

        if _1816.LoadedToroidalRollerBearingResults.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast loaded_bearing to LoadedToroidalRollerBearingResults. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lamina_dynamic_equivalent_loads(self) -> 'List[_1732.ForceAtLaminaGroupReportable]':
        """List[ForceAtLaminaGroupReportable]: 'LaminaDynamicEquivalentLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LaminaDynamicEquivalentLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
