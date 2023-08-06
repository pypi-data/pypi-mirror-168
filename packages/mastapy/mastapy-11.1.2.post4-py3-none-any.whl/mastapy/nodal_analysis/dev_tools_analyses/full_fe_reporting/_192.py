"""_192.py

ElementPropertiesShell
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.fe_tools.vis_tools_global.vis_tools_global_enums import _1189
from mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting import _195
from mastapy._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_SHELL = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting', 'ElementPropertiesShell')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementPropertiesShell',)


class ElementPropertiesShell(_195.ElementPropertiesWithMaterial):
    """ElementPropertiesShell

    This is a mastapy class.
    """

    TYPE = _ELEMENT_PROPERTIES_SHELL

    def __init__(self, instance_to_wrap: 'ElementPropertiesShell.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_shear_ratio(self) -> 'float':
        """float: 'EffectiveShearRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveShearRatio

        if temp is None:
            return None

        return temp

    @property
    def layer_thicknesses(self) -> 'str':
        """str: 'LayerThicknesses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LayerThicknesses

        if temp is None:
            return None

        return temp

    @property
    def number_of_layers(self) -> 'int':
        """int: 'NumberOfLayers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfLayers

        if temp is None:
            return None

        return temp

    @property
    def thickness(self) -> 'float':
        """float: 'Thickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Thickness

        if temp is None:
            return None

        return temp

    @property
    def wall_type(self) -> '_1189.ElementPropertiesShellWallType':
        """ElementPropertiesShellWallType: 'WallType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WallType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1189.ElementPropertiesShellWallType)(value) if value is not None else None
