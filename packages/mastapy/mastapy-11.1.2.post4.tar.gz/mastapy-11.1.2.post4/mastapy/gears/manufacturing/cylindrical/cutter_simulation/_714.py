"""_714.py

WormGrinderSimulationCalculator
"""


from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _694
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _709
from mastapy._internal.python_net import python_net_import

_WORM_GRINDER_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'WormGrinderSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGrinderSimulationCalculator',)


class WormGrinderSimulationCalculator(_709.RackSimulationCalculator):
    """WormGrinderSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _WORM_GRINDER_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'WormGrinderSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def worm_grinder(self) -> '_694.CylindricalGearWormGrinderShape':
        """CylindricalGearWormGrinderShape: 'WormGrinder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGrinder

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
