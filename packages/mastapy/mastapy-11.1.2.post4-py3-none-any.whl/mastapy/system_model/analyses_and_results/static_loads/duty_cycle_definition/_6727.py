"""_6727.py

RampOrSteadyStateInputOptions
"""


from mastapy.utility_gui import _1622
from mastapy._internal.python_net import python_net_import

_RAMP_OR_STEADY_STATE_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'RampOrSteadyStateInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('RampOrSteadyStateInputOptions',)


class RampOrSteadyStateInputOptions(_1622.ColumnInputOptions):
    """RampOrSteadyStateInputOptions

    This is a mastapy class.
    """

    TYPE = _RAMP_OR_STEADY_STATE_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'RampOrSteadyStateInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
