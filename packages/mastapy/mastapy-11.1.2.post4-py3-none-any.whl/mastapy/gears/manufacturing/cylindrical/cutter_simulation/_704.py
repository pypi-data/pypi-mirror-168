"""_704.py

FormWheelGrindingSimulationCalculator
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _690
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _697
from mastapy._internal.python_net import python_net_import

_FORM_WHEEL_GRINDING_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'FormWheelGrindingSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('FormWheelGrindingSimulationCalculator',)


class FormWheelGrindingSimulationCalculator(_697.CutterSimulationCalc):
    """FormWheelGrindingSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _FORM_WHEEL_GRINDING_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'FormWheelGrindingSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @property
    def transverse_root_fillet_radius(self) -> 'float':
        """float: 'TransverseRootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseRootFilletRadius

        if temp is None:
            return None

        return temp

    @property
    def profiled_grinding_wheel(self) -> '_690.CylindricalGearFormedWheelGrinderTangible':
        """CylindricalGearFormedWheelGrinderTangible: 'ProfiledGrindingWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfiledGrindingWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
