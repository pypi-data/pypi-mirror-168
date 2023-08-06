"""_6382.py

SynchroniserCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.couplings import _2351
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6696
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6367
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'SynchroniserCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCriticalSpeedAnalysis',)


class SynchroniserCriticalSpeedAnalysis(_6367.SpecialisedAssemblyCriticalSpeedAnalysis):
    """SynchroniserCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'SynchroniserCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2351.Synchroniser':
        """Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6696.SynchroniserLoadCase':
        """SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
