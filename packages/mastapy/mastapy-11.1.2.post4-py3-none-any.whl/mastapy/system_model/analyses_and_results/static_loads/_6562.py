"""_6562.py

ConceptCouplingHalfLoadCase
"""


from mastapy.system_model.part_model.couplings import _2331
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6575
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConceptCouplingHalfLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfLoadCase',)


class ConceptCouplingHalfLoadCase(_6575.CouplingHalfLoadCase):
    """ConceptCouplingHalfLoadCase

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_HALF_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2331.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
