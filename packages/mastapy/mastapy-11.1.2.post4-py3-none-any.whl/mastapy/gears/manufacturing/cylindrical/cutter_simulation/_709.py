"""_709.py

RackSimulationCalculator
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _697
from mastapy._internal.python_net import python_net_import

_RACK_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'RackSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('RackSimulationCalculator',)


class RackSimulationCalculator(_697.CutterSimulationCalc):
    """RackSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _RACK_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'RackSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hob_working_depth_delta(self) -> 'float':
        """float: 'HobWorkingDepthDelta' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HobWorkingDepthDelta

        if temp is None:
            return None

        return temp
