"""_4464.py

SingleModeResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4460, _4456
from mastapy._internal.python_net import python_net_import

_SINGLE_MODE_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'SingleModeResults')


__docformat__ = 'restructuredtext en'
__all__ = ('SingleModeResults',)


class SingleModeResults(_4456.DesignEntityModalAnalysisGroupResults):
    """SingleModeResults

    This is a mastapy class.
    """

    TYPE = _SINGLE_MODE_RESULTS

    def __init__(self, instance_to_wrap: 'SingleModeResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mode_frequency(self) -> 'float':
        """float: 'ModeFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeFrequency

        if temp is None:
            return None

        return temp

    @property
    def mode_id(self) -> 'int':
        """int: 'ModeID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeID

        if temp is None:
            return None

        return temp

    @property
    def all_rigidly_connected_groups(self) -> 'List[_4460.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]':
        """List[RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]: 'AllRigidlyConnectedGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllRigidlyConnectedGroups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rigidly_connected_groups_with_significant_energy(self) -> 'List[_4460.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]':
        """List[RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]: 'RigidlyConnectedGroupsWithSignificantEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RigidlyConnectedGroupsWithSignificantEnergy

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rigidly_connected_groups_with_significant_kinetic_energy(self) -> 'List[_4460.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]':
        """List[RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]: 'RigidlyConnectedGroupsWithSignificantKineticEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RigidlyConnectedGroupsWithSignificantKineticEnergy

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rigidly_connected_groups_with_significant_strain_energy(self) -> 'List[_4460.RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]':
        """List[RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis]: 'RigidlyConnectedGroupsWithSignificantStrainEnergy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RigidlyConnectedGroupsWithSignificantStrainEnergy

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
