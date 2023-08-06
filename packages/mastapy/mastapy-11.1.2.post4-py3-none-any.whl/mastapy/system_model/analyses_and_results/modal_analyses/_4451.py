"""_4451.py

ZerolBevelGearModalAnalysis
"""


from mastapy.system_model.part_model.gears import _2302
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6713
from mastapy.system_model.analyses_and_results.system_deflections import _2585
from mastapy.system_model.analyses_and_results.modal_analyses import _4329
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ZerolBevelGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearModalAnalysis',)


class ZerolBevelGearModalAnalysis(_4329.BevelGearModalAnalysis):
    """ZerolBevelGearModalAnalysis

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'ZerolBevelGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2302.ZerolBevelGear':
        """ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6713.ZerolBevelGearLoadCase':
        """ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2585.ZerolBevelGearSystemDeflection':
        """ZerolBevelGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
