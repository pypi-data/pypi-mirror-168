"""_711.py

ShaperSimulationCalculator
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _692
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _697
from mastapy._internal.python_net import python_net_import

_SHAPER_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'ShaperSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaperSimulationCalculator',)


class ShaperSimulationCalculator(_697.CutterSimulationCalc):
    """ShaperSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _SHAPER_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'ShaperSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cutting_centre_distance(self) -> 'float':
        """float: 'CuttingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CuttingCentreDistance

        if temp is None:
            return None

        return temp

    @property
    def cutting_pressure_angle(self) -> 'float':
        """float: 'CuttingPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CuttingPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def shaper_sap_diameter(self) -> 'float':
        """float: 'ShaperSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaperSAPDiameter

        if temp is None:
            return None

        return temp

    @property
    def shaper(self) -> '_692.CylindricalGearShaperTangible':
        """CylindricalGearShaperTangible: 'Shaper' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaper

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
