"""_4092.py

DutyCycleResultsForRootAssembly
"""


from mastapy.system_model.analyses_and_results.system_deflections.compound import _2647
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForRootAssembly')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForRootAssembly',)


class DutyCycleResultsForRootAssembly(_0.APIBase):
    """DutyCycleResultsForRootAssembly

    This is a mastapy class.
    """

    TYPE = _DUTY_CYCLE_RESULTS_FOR_ROOT_ASSEMBLY

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForRootAssembly.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_efficiency_results(self) -> '_2647.DutyCycleEfficiencyResults':
        """DutyCycleEfficiencyResults: 'DutyCycleEfficiencyResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DutyCycleEfficiencyResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
