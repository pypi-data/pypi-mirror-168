"""_5848.py

SynchroniserHalfHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.part_model.couplings import _2353
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6695
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5850
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SynchroniserHalfHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfHarmonicAnalysisOfSingleExcitation',)


class SynchroniserHalfHarmonicAnalysisOfSingleExcitation(_5850.SynchroniserPartHarmonicAnalysisOfSingleExcitation):
    """SynchroniserHalfHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'SynchroniserHalfHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2353.SynchroniserHalf':
        """SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6695.SynchroniserHalfLoadCase':
        """SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
