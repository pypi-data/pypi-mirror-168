"""_6660.py

PlanetaryGearSetLoadCase
"""


from mastapy.utility import _1393
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.part_model.gears import _2291
from mastapy.system_model.analyses_and_results.static_loads import _6588
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PlanetaryGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetLoadCase',)


class PlanetaryGearSetLoadCase(_6588.CylindricalGearSetLoadCase):
    """PlanetaryGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _PLANETARY_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_gear_blank_elastic_distortion(self) -> '_1393.LoadCaseOverrideOption':
        """LoadCaseOverrideOption: 'IncludeGearBlankElasticDistortion' is the original name of this property."""

        temp = self.wrapped.IncludeGearBlankElasticDistortion

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1393.LoadCaseOverrideOption)(value) if value is not None else None

    @include_gear_blank_elastic_distortion.setter
    def include_gear_blank_elastic_distortion(self, value: '_1393.LoadCaseOverrideOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeGearBlankElasticDistortion = value

    @property
    def specify_separate_micro_geometry_for_each_planet_gear(self) -> 'bool':
        """bool: 'SpecifySeparateMicroGeometryForEachPlanetGear' is the original name of this property."""

        temp = self.wrapped.SpecifySeparateMicroGeometryForEachPlanetGear

        if temp is None:
            return None

        return temp

    @specify_separate_micro_geometry_for_each_planet_gear.setter
    def specify_separate_micro_geometry_for_each_planet_gear(self, value: 'bool'):
        self.wrapped.SpecifySeparateMicroGeometryForEachPlanetGear = bool(value) if value else False

    @property
    def assembly_design(self) -> '_2291.PlanetaryGearSet':
        """PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
