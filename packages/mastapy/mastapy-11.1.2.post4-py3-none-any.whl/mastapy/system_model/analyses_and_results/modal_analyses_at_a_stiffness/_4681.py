"""_4681.py

PointLoadModalAnalysisAtAStiffness
"""


from mastapy.system_model.part_model import _2221
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6665
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4717
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'PointLoadModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadModalAnalysisAtAStiffness',)


class PointLoadModalAnalysisAtAStiffness(_4717.VirtualComponentModalAnalysisAtAStiffness):
    """PointLoadModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _POINT_LOAD_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'PointLoadModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2221.PointLoad':
        """PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6665.PointLoadLoadCase':
        """PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
