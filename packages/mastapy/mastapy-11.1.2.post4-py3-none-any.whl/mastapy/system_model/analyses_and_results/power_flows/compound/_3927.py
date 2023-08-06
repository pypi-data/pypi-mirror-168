"""_3927.py

BoltedJointCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model import _2194
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3793
from mastapy.system_model.analyses_and_results.power_flows.compound import _4005
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BoltedJointCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointCompoundPowerFlow',)


class BoltedJointCompoundPowerFlow(_4005.SpecialisedAssemblyCompoundPowerFlow):
    """BoltedJointCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _BOLTED_JOINT_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'BoltedJointCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2194.BoltedJoint':
        """BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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
    def assembly_analysis_cases_ready(self) -> 'List[_3793.BoltedJointPowerFlow]':
        """List[BoltedJointPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_3793.BoltedJointPowerFlow]':
        """List[BoltedJointPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
