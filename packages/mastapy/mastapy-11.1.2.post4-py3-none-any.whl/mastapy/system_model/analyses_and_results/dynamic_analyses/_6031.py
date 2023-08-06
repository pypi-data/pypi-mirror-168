"""_6031.py

ConceptGearDynamicAnalysis
"""


from mastapy.system_model.part_model.gears import _2270
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6564
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6061
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearDynamicAnalysis',)


class ConceptGearDynamicAnalysis(_6061.GearDynamicAnalysis):
    """ConceptGearDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2270.ConceptGear':
        """ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6564.ConceptGearLoadCase':
        """ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
