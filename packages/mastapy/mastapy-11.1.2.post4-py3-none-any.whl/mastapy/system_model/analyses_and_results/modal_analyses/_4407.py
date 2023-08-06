"""_4407.py

RingPinsModalAnalysis
"""


from mastapy.system_model.part_model.cycloidal import _2319
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6670
from mastapy.system_model.analyses_and_results.system_deflections import _2538
from mastapy.system_model.analyses_and_results.modal_analyses import _4394
from mastapy._internal.python_net import python_net_import

_RING_PINS_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'RingPinsModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsModalAnalysis',)


class RingPinsModalAnalysis(_4394.MountableComponentModalAnalysis):
    """RingPinsModalAnalysis

    This is a mastapy class.
    """

    TYPE = _RING_PINS_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'RingPinsModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2319.RingPins':
        """RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6670.RingPinsLoadCase':
        """RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2538.RingPinsSystemDeflection':
        """RingPinsSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
