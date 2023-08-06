"""_1565.py

LegacyChartDefinition
"""


from mastapy.utility.report import _1529
from mastapy._internal.python_net import python_net_import

_LEGACY_CHART_DEFINITION = python_net_import('SMT.MastaAPI.Utility.Report', 'LegacyChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('LegacyChartDefinition',)


class LegacyChartDefinition(_1529.ChartDefinition):
    """LegacyChartDefinition

    This is a mastapy class.
    """

    TYPE = _LEGACY_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'LegacyChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
