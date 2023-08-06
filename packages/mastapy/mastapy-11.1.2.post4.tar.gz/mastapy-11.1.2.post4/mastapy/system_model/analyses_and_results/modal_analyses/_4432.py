"""_4432.py

SynchroniserHalfModalAnalysis
"""


from mastapy.system_model.part_model.couplings import _2353
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6695
from mastapy.system_model.analyses_and_results.system_deflections import _2565
from mastapy.system_model.analyses_and_results.modal_analyses import _4434
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'SynchroniserHalfModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfModalAnalysis',)


class SynchroniserHalfModalAnalysis(_4434.SynchroniserPartModalAnalysis):
    """SynchroniserHalfModalAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_HALF_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserHalfModalAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2565.SynchroniserHalfSystemDeflection':
        """SynchroniserHalfSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
