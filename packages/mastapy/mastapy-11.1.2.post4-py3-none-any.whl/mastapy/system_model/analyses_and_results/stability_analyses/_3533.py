"""_3533.py

ConceptCouplingConnectionStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2095
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6561
from mastapy.system_model.analyses_and_results.stability_analyses import _3544
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptCouplingConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionStabilityAnalysis',)


class ConceptCouplingConnectionStabilityAnalysis(_3544.CouplingConnectionStabilityAnalysis):
    """ConceptCouplingConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2095.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6561.ConceptCouplingConnectionLoadCase':
        """ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
