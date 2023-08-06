"""_4940.py

PowerLoadModalAnalysisAtASpeed
"""


from mastapy.system_model.part_model import _2222
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6666
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4975
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PowerLoadModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadModalAnalysisAtASpeed',)


class PowerLoadModalAnalysisAtASpeed(_4975.VirtualComponentModalAnalysisAtASpeed):
    """PowerLoadModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'PowerLoadModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2222.PowerLoad':
        """PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6666.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
