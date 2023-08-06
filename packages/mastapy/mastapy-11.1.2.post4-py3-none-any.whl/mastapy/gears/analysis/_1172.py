"""_1172.py

GearImplementationAnalysisDutyCycle
"""


from mastapy.gears.analysis import _1170
from mastapy._internal.python_net import python_net_import

_GEAR_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearImplementationAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('GearImplementationAnalysisDutyCycle',)


class GearImplementationAnalysisDutyCycle(_1170.GearDesignAnalysis):
    """GearImplementationAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE = _GEAR_IMPLEMENTATION_ANALYSIS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'GearImplementationAnalysisDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
