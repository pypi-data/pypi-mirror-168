"""_6561.py

ConceptCouplingConnectionLoadCase
"""


from mastapy.system_model.connections_and_sockets.couplings import _2095
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6574
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionLoadCase',)


class ConceptCouplingConnectionLoadCase(_6574.CouplingConnectionLoadCase):
    """ConceptCouplingConnectionLoadCase

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionLoadCase.TYPE'):
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
