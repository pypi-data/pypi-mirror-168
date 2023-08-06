"""_992.py

CylindricalGearSetMacroGeometryOptimiser
"""


from mastapy._internal import constructor
from mastapy.gears import _304
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MACRO_GEOMETRY_OPTIMISER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearSetMacroGeometryOptimiser')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMacroGeometryOptimiser',)


class CylindricalGearSetMacroGeometryOptimiser(_304.GearSetOptimiser):
    """CylindricalGearSetMacroGeometryOptimiser

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_MACRO_GEOMETRY_OPTIMISER

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMacroGeometryOptimiser.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def helix_angle(self) -> 'float':
        """float: 'HelixAngle' is the original name of this property."""

        temp = self.wrapped.HelixAngle

        if temp is None:
            return None

        return temp

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def modify_basic_rack(self) -> 'bool':
        """bool: 'ModifyBasicRack' is the original name of this property."""

        temp = self.wrapped.ModifyBasicRack

        if temp is None:
            return None

        return temp

    @modify_basic_rack.setter
    def modify_basic_rack(self, value: 'bool'):
        self.wrapped.ModifyBasicRack = bool(value) if value else False

    @property
    def normal_module(self) -> 'float':
        """float: 'NormalModule' is the original name of this property."""

        temp = self.wrapped.NormalModule

        if temp is None:
            return None

        return temp

    @normal_module.setter
    def normal_module(self, value: 'float'):
        self.wrapped.NormalModule = float(value) if value else 0.0

    @property
    def normal_pressure_angle(self) -> 'float':
        """float: 'NormalPressureAngle' is the original name of this property."""

        temp = self.wrapped.NormalPressureAngle

        if temp is None:
            return None

        return temp

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def root_gear_profile_shift_coefficient(self) -> 'float':
        """float: 'RootGearProfileShiftCoefficient' is the original name of this property."""

        temp = self.wrapped.RootGearProfileShiftCoefficient

        if temp is None:
            return None

        return temp

    @root_gear_profile_shift_coefficient.setter
    def root_gear_profile_shift_coefficient(self, value: 'float'):
        self.wrapped.RootGearProfileShiftCoefficient = float(value) if value else 0.0

    @property
    def root_gear_thickness_reduction(self) -> 'float':
        """float: 'RootGearThicknessReduction' is the original name of this property."""

        temp = self.wrapped.RootGearThicknessReduction

        if temp is None:
            return None

        return temp

    @root_gear_thickness_reduction.setter
    def root_gear_thickness_reduction(self, value: 'float'):
        self.wrapped.RootGearThicknessReduction = float(value) if value else 0.0

    @property
    def helix_angle_input_is_active(self) -> 'bool':
        """bool: 'HelixAngleInputIsActive' is the original name of this property."""

        temp = self.wrapped.HelixAngleInputIsActive

        if temp is None:
            return None

        return temp

    @helix_angle_input_is_active.setter
    def helix_angle_input_is_active(self, value: 'bool'):
        self.wrapped.HelixAngleInputIsActive = bool(value) if value else False

    @property
    def pressure_angle_input_is_active(self) -> 'bool':
        """bool: 'PressureAngleInputIsActive' is the original name of this property."""

        temp = self.wrapped.PressureAngleInputIsActive

        if temp is None:
            return None

        return temp

    @pressure_angle_input_is_active.setter
    def pressure_angle_input_is_active(self, value: 'bool'):
        self.wrapped.PressureAngleInputIsActive = bool(value) if value else False
