"""_1629.py

NDChartDefinition
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1529
from mastapy._internal.python_net import python_net_import

_ND_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'NDChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('NDChartDefinition',)


class NDChartDefinition(_1529.ChartDefinition):
    """NDChartDefinition

    This is a mastapy class.
    """

    TYPE = _ND_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'NDChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def specify_shared_chart_settings(self) -> 'bool':
        """bool: 'SpecifySharedChartSettings' is the original name of this property."""

        temp = self.wrapped.SpecifySharedChartSettings

        if temp is None:
            return None

        return temp

    @specify_shared_chart_settings.setter
    def specify_shared_chart_settings(self, value: 'bool'):
        self.wrapped.SpecifySharedChartSettings = bool(value) if value else False
