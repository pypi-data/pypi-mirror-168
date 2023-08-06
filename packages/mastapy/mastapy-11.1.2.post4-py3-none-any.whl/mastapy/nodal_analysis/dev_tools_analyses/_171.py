"""_171.py

FEModelStaticAnalysisDrawStyle
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import _172
from mastapy._internal.python_net import python_net_import

_FE_MODEL_STATIC_ANALYSIS_DRAW_STYLE = python_net_import('SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses', 'FEModelStaticAnalysisDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('FEModelStaticAnalysisDrawStyle',)


class FEModelStaticAnalysisDrawStyle(_172.FEModelTabDrawStyle):
    """FEModelStaticAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE = _FE_MODEL_STATIC_ANALYSIS_DRAW_STYLE

    def __init__(self, instance_to_wrap: 'FEModelStaticAnalysisDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def show_force_arrows(self) -> 'bool':
        """bool: 'ShowForceArrows' is the original name of this property."""

        temp = self.wrapped.ShowForceArrows

        if temp is None:
            return None

        return temp

    @show_force_arrows.setter
    def show_force_arrows(self, value: 'bool'):
        self.wrapped.ShowForceArrows = bool(value) if value else False
