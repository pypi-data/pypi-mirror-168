"""_288.py

BevelHypoidGearDesignSettings
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears import _316
from mastapy.utility import _1395
from mastapy._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_DESIGN_SETTINGS = python_net_import('SMT.MastaAPI.Gears', 'BevelHypoidGearDesignSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelHypoidGearDesignSettings',)


class BevelHypoidGearDesignSettings(_1395.PerMachineSettings):
    """BevelHypoidGearDesignSettings

    This is a mastapy class.
    """

    TYPE = _BEVEL_HYPOID_GEAR_DESIGN_SETTINGS

    def __init__(self, instance_to_wrap: 'BevelHypoidGearDesignSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(self) -> 'bool':
        """bool: 'AllowOverridingManufacturingConfigMicroGeometryInALoadCase' is the original name of this property."""

        temp = self.wrapped.AllowOverridingManufacturingConfigMicroGeometryInALoadCase

        if temp is None:
            return None

        return temp

    @allow_overriding_manufacturing_config_micro_geometry_in_a_load_case.setter
    def allow_overriding_manufacturing_config_micro_geometry_in_a_load_case(self, value: 'bool'):
        self.wrapped.AllowOverridingManufacturingConfigMicroGeometryInALoadCase = bool(value) if value else False

    @property
    def minimum_ratio(self) -> 'float':
        """float: 'MinimumRatio' is the original name of this property."""

        temp = self.wrapped.MinimumRatio

        if temp is None:
            return None

        return temp

    @minimum_ratio.setter
    def minimum_ratio(self, value: 'float'):
        self.wrapped.MinimumRatio = float(value) if value else 0.0

    @property
    def quality_grade_type(self) -> '_316.QualityGradeTypes':
        """QualityGradeTypes: 'QualityGradeType' is the original name of this property."""

        temp = self.wrapped.QualityGradeType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_316.QualityGradeTypes)(value) if value is not None else None

    @quality_grade_type.setter
    def quality_grade_type(self, value: '_316.QualityGradeTypes'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.QualityGradeType = value
