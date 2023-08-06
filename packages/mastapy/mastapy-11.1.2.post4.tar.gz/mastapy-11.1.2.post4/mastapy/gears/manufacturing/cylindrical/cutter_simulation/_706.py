"""_706.py

HobSimulationCalculator
"""


from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _691
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _709
from mastapy._internal.python_net import python_net_import

_HOB_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'HobSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('HobSimulationCalculator',)


class HobSimulationCalculator(_709.RackSimulationCalculator):
    """HobSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _HOB_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'HobSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def hob(self) -> '_691.CylindricalGearHobShape':
        """CylindricalGearHobShape: 'Hob' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Hob

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
