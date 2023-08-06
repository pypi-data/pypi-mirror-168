"""_3529.py

ClutchHalfStabilityAnalysis
"""


from mastapy.system_model.part_model.couplings import _2328
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6557
from mastapy.system_model.analyses_and_results.stability_analyses import _3545
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ClutchHalfStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfStabilityAnalysis',)


class ClutchHalfStabilityAnalysis(_3545.CouplingHalfStabilityAnalysis):
    """ClutchHalfStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchHalfStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2328.ClutchHalf':
        """ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6557.ClutchHalfLoadCase':
        """ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
