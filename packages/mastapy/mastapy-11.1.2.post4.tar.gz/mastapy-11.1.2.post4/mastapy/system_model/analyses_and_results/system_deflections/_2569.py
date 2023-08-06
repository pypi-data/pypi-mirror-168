"""_2569.py

SystemDeflection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2571, _2521
from mastapy.system_model.fe import _2157
from mastapy.system_model.analyses_and_results.analysis_cases import _7270
from mastapy._internal.python_net import python_net_import

_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDeflection',)


class SystemDeflection(_7270.FEAnalysis):
    """SystemDeflection

    This is a mastapy class.
    """

    TYPE = _SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'SystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def current_time(self) -> 'float':
        """float: 'CurrentTime' is the original name of this property."""

        temp = self.wrapped.CurrentTime

        if temp is None:
            return None

        return temp

    @current_time.setter
    def current_time(self, value: 'float'):
        self.wrapped.CurrentTime = float(value) if value else 0.0

    @property
    def include_twist_in_misalignments(self) -> 'bool':
        """bool: 'IncludeTwistInMisalignments' is the original name of this property."""

        temp = self.wrapped.IncludeTwistInMisalignments

        if temp is None:
            return None

        return temp

    @include_twist_in_misalignments.setter
    def include_twist_in_misalignments(self, value: 'bool'):
        self.wrapped.IncludeTwistInMisalignments = bool(value) if value else False

    @property
    def iterations(self) -> 'int':
        """int: 'Iterations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Iterations

        if temp is None:
            return None

        return temp

    @property
    def largest_power_across_a_connection(self) -> 'float':
        """float: 'LargestPowerAcrossAConnection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LargestPowerAcrossAConnection

        if temp is None:
            return None

        return temp

    @property
    def maximum_circulating_power(self) -> 'float':
        """float: 'MaximumCirculatingPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumCirculatingPower

        if temp is None:
            return None

        return temp

    @property
    def power_convergence_error(self) -> 'float':
        """float: 'PowerConvergenceError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerConvergenceError

        if temp is None:
            return None

        return temp

    @property
    def power_error(self) -> 'float':
        """float: 'PowerError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerError

        if temp is None:
            return None

        return temp

    @property
    def power_lost(self) -> 'float':
        """float: 'PowerLost' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLost

        if temp is None:
            return None

        return temp

    @property
    def total_input_power(self) -> 'float':
        """float: 'TotalInputPower' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalInputPower

        if temp is None:
            return None

        return temp

    @property
    def total_load_dependent_power_loss(self) -> 'float':
        """float: 'TotalLoadDependentPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalLoadDependentPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def total_speed_dependent_power_loss(self) -> 'float':
        """float: 'TotalSpeedDependentPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalSpeedDependentPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def analysis_options(self) -> '_2571.SystemDeflectionOptions':
        """SystemDeflectionOptions: 'AnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def overall_efficiency_results(self) -> '_2521.LoadCaseOverallEfficiencyResult':
        """LoadCaseOverallEfficiencyResult: 'OverallEfficiencyResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverallEfficiencyResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_race_f_es(self) -> 'List[_2157.RaceBearingFESystemDeflection]':
        """List[RaceBearingFESystemDeflection]: 'BearingRaceFEs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingRaceFEs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
