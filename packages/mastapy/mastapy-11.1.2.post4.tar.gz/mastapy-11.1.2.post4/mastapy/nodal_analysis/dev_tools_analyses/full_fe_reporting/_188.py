"""_188.py

ElementPropertiesBeam
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.fe_tools.vis_tools_global.vis_tools_global_enums import _1186
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _195
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_BEAM = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesBeam')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesBeam',)


class ElementPropertiesBeam(_195.ElementPropertiesWithMaterial):
    """ElementPropertiesBeam

    This is a mastapy class.
    """

    TYPE = _ELEMENT_PROPERTIES_BEAM

    def __init__(self, instance_to_wrap: 'ElementPropertiesBeam.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def section_dimensions(self) -> 'str':
        """str: 'SectionDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionDimensions

        if temp is None:
            return None

        return temp

    @property
    def section_type(self) -> '_1186.BeamSectionType':
        """BeamSectionType: 'SectionType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1186.BeamSectionType)(value) if value is not None else None
