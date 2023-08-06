"""_1182.py

GearSetImplementationAnalysisDutyCycle
"""


from mastapy._internal import constructor
from mastapy.gears.analysis import _1181
from mastapy._internal.python_net import python_net_import

_GEAR_SET_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearSetImplementationAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetImplementationAnalysisDutyCycle',)


class GearSetImplementationAnalysisDutyCycle(_1181.GearSetImplementationAnalysisAbstract):
    """GearSetImplementationAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'GearSetImplementationAnalysisDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_name(self) -> 'str':
        """str: 'DutyCycleName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DutyCycleName

        if temp is None:
            return None

        return temp
