"""_2647.py

DutyCycleEfficiencyResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2521
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_EFFICIENCY_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'DutyCycleEfficiencyResults')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleEfficiencyResults',)


class DutyCycleEfficiencyResults(_0.APIBase):
    """DutyCycleEfficiencyResults

    This is a mastapy class.
    """

    TYPE = _DUTY_CYCLE_EFFICIENCY_RESULTS

    def __init__(self, instance_to_wrap: 'DutyCycleEfficiencyResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def efficiency(self) -> 'float':
        """float: 'Efficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Efficiency

        if temp is None:
            return None

        return temp

    @property
    def energy_input(self) -> 'float':
        """float: 'EnergyInput' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyInput

        if temp is None:
            return None

        return temp

    @property
    def energy_lost(self) -> 'float':
        """float: 'EnergyLost' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyLost

        if temp is None:
            return None

        return temp

    @property
    def energy_output(self) -> 'float':
        """float: 'EnergyOutput' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyOutput

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def load_case_overall_efficiency_result(self) -> 'List[_2521.LoadCaseOverallEfficiencyResult]':
        """List[LoadCaseOverallEfficiencyResult]: 'LoadCaseOverallEfficiencyResult' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCaseOverallEfficiencyResult

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
