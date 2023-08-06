"""_1059.py

CylindricalGearMicroGeometry
"""


from typing import List

from mastapy.utility.report import _1565
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _975, _1002, _987
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1054, _1077
from mastapy.gears.analysis import _1173
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMicroGeometry',)


class CylindricalGearMicroGeometry(_1173.GearImplementationDetail):
    """CylindricalGearMicroGeometry

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MICRO_GEOMETRY

    def __init__(self, instance_to_wrap: 'CylindricalGearMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lead_form_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'LeadFormChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadFormChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lead_slope_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'LeadSlopeChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadSlopeChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lead_total_nominal_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'LeadTotalNominalChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadTotalNominalChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lead_total_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'LeadTotalChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadTotalChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_control_point_is_user_specified(self) -> 'bool':
        """bool: 'ProfileControlPointIsUserSpecified' is the original name of this property."""

        temp = self.wrapped.ProfileControlPointIsUserSpecified

        if temp is None:
            return None

        return temp

    @profile_control_point_is_user_specified.setter
    def profile_control_point_is_user_specified(self, value: 'bool'):
        self.wrapped.ProfileControlPointIsUserSpecified = bool(value) if value else False

    @property
    def profile_form_10_percent_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileForm10PercentChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileForm10PercentChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_form_50_percent_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileForm50PercentChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileForm50PercentChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_form_90_percent_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileForm90PercentChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileForm90PercentChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_form_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileFormChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileFormChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_total_nominal_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileTotalNominalChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileTotalNominalChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_total_chart(self) -> '_1565.LegacyChartDefinition':
        """LegacyChartDefinition: 'ProfileTotalChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileTotalChart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def use_same_micro_geometry_on_both_flanks(self) -> 'bool':
        """bool: 'UseSameMicroGeometryOnBothFlanks' is the original name of this property."""

        temp = self.wrapped.UseSameMicroGeometryOnBothFlanks

        if temp is None:
            return None

        return temp

    @use_same_micro_geometry_on_both_flanks.setter
    def use_same_micro_geometry_on_both_flanks(self, value: 'bool'):
        self.wrapped.UseSameMicroGeometryOnBothFlanks = bool(value) if value else False

    @property
    def cylindrical_gear(self) -> '_975.CylindricalGearDesign':
        """CylindricalGearDesign: 'CylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGear

        if temp is None:
            return None

        if _975.CylindricalGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_gear to CylindricalGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank(self) -> '_1054.CylindricalGearFlankMicroGeometry':
        """CylindricalGearFlankMicroGeometry: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def profile_control_point(self) -> '_987.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileControlPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileControlPoint

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_1054.CylindricalGearFlankMicroGeometry':
        """CylindricalGearFlankMicroGeometry: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def flanks(self) -> 'List[_1054.CylindricalGearFlankMicroGeometry]':
        """List[CylindricalGearFlankMicroGeometry]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Flanks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshed_gears(self) -> 'List[_1077.MeshedCylindricalGearMicroGeometry]':
        """List[MeshedCylindricalGearMicroGeometry]: 'MeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshedGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def both_flanks(self) -> '_1054.CylindricalGearFlankMicroGeometry':
        """CylindricalGearFlankMicroGeometry: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BothFlanks

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
