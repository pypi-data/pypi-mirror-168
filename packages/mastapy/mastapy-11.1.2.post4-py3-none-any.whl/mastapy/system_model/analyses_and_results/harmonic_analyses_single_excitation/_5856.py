"""_5856.py

UnbalancedMassHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.part_model import _2227
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6708
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5857
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'UnbalancedMassHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassHarmonicAnalysisOfSingleExcitation',)


class UnbalancedMassHarmonicAnalysisOfSingleExcitation(_5857.VirtualComponentHarmonicAnalysisOfSingleExcitation):
    """UnbalancedMassHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _UNBALANCED_MASS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'UnbalancedMassHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2227.UnbalancedMass':
        """UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6708.UnbalancedMassLoadCase':
        """UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
