"""_713.py

VirtualSimulationCalculator
"""


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _697
from mastapy._internal.python_net import python_net_import

_VIRTUAL_SIMULATION_CALCULATOR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'VirtualSimulationCalculator')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualSimulationCalculator',)


class VirtualSimulationCalculator(_697.CutterSimulationCalc):
    """VirtualSimulationCalculator

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_SIMULATION_CALCULATOR

    def __init__(self, instance_to_wrap: 'VirtualSimulationCalculator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_moment_arm_for_iso_rating_worst(self) -> 'float':
        """float: 'BendingMomentArmForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingMomentArmForISORatingWorst

        if temp is None:
            return None

        return temp

    @property
    def form_factor_for_iso_rating_worst(self) -> 'float':
        """float: 'FormFactorForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormFactorForISORatingWorst

        if temp is None:
            return None

        return temp

    @property
    def radius_of_critical_point_for_iso_rating_worst(self) -> 'float':
        """float: 'RadiusOfCriticalPointForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadiusOfCriticalPointForISORatingWorst

        if temp is None:
            return None

        return temp

    @property
    def root_fillet_radius_for_agma_rating(self) -> 'float':
        """float: 'RootFilletRadiusForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFilletRadiusForAGMARating

        if temp is None:
            return None

        return temp

    @property
    def root_fillet_radius_for_iso_rating(self) -> 'float':
        """float: 'RootFilletRadiusForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFilletRadiusForISORating

        if temp is None:
            return None

        return temp

    @property
    def root_fillet_radius_for_iso_rating_worst(self) -> 'float':
        """float: 'RootFilletRadiusForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFilletRadiusForISORatingWorst

        if temp is None:
            return None

        return temp

    @property
    def stress_correction_form_factor_worst(self) -> 'float':
        """float: 'StressCorrectionFormFactorWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFormFactorWorst

        if temp is None:
            return None

        return temp

    @property
    def stress_correction_factor_for_iso_rating_worst(self) -> 'float':
        """float: 'StressCorrectionFactorForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCorrectionFactorForISORatingWorst

        if temp is None:
            return None

        return temp

    @property
    def tooth_root_chord_for_iso_rating(self) -> 'float':
        """float: 'ToothRootChordForISORating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootChordForISORating

        if temp is None:
            return None

        return temp

    @property
    def tooth_root_chord_for_iso_rating_worst(self) -> 'float':
        """float: 'ToothRootChordForISORatingWorst' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootChordForISORatingWorst

        if temp is None:
            return None

        return temp
