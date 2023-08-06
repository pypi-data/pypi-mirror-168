"""_6022.py

BoltedJointDynamicAnalysis
"""


from mastapy.system_model.part_model import _2194
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6554
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6101
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'BoltedJointDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointDynamicAnalysis',)


class BoltedJointDynamicAnalysis(_6101.SpecialisedAssemblyDynamicAnalysis):
    """BoltedJointDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _BOLTED_JOINT_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'BoltedJointDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2194.BoltedJoint':
        """BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6554.BoltedJointLoadCase':
        """BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
