"""_6825.py

PowerLoadAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.part_model import _2222
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6666
from mastapy.system_model.analyses_and_results.system_deflections import _2536
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6860
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'PowerLoadAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadAdvancedTimeSteppingAnalysisForModulation',)


class PowerLoadAdvancedTimeSteppingAnalysisForModulation(_6860.VirtualComponentAdvancedTimeSteppingAnalysisForModulation):
    """PowerLoadAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'PowerLoadAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2536.PowerLoadSystemDeflection':
        """PowerLoadSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
