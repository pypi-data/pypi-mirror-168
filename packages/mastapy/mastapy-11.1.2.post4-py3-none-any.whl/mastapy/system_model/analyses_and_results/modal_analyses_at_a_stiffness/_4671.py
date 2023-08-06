"""_4671.py

MeasurementComponentModalAnalysisAtAStiffness
"""


from mastapy.system_model.part_model import _2213
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6648
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4717
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'MeasurementComponentModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentModalAnalysisAtAStiffness',)


class MeasurementComponentModalAnalysisAtAStiffness(_4717.VirtualComponentModalAnalysisAtAStiffness):
    """MeasurementComponentModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_COMPONENT_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'MeasurementComponentModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2213.MeasurementComponent':
        """MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6648.MeasurementComponentLoadCase':
        """MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
