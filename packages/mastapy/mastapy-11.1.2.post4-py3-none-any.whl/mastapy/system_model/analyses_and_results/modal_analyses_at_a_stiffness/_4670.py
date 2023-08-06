"""_4670.py

MassDiscModalAnalysisAtAStiffness
"""


from typing import List

from mastapy.system_model.part_model import _2212
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6647
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4717
from mastapy._internal.python_net import python_net_import

_MASS_DISC_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'MassDiscModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscModalAnalysisAtAStiffness',)


class MassDiscModalAnalysisAtAStiffness(_4717.VirtualComponentModalAnalysisAtAStiffness):
    """MassDiscModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _MASS_DISC_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'MassDiscModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2212.MassDisc':
        """MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6647.MassDiscLoadCase':
        """MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[MassDiscModalAnalysisAtAStiffness]':
        """List[MassDiscModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
