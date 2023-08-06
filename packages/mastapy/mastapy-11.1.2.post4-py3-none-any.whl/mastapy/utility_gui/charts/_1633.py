"""_1633.py

ThreeDVectorChartDefinition
"""


from mastapy.utility_gui.charts import _1629
from mastapy._internal.python_net import python_net_import

_THREE_D_VECTOR_CHART_DEFINITION = python_net_import('SMT.MastaAPI.UtilityGUI.Charts', 'ThreeDVectorChartDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('ThreeDVectorChartDefinition',)


class ThreeDVectorChartDefinition(_1629.NDChartDefinition):
    """ThreeDVectorChartDefinition

    This is a mastapy class.
    """

    TYPE = _THREE_D_VECTOR_CHART_DEFINITION

    def __init__(self, instance_to_wrap: 'ThreeDVectorChartDefinition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
