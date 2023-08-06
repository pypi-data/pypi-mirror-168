"""_672.py

CylindricalGearAbstractCutterDesign
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_ABSTRACT_CUTTER_DESIGN = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearAbstractCutterDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearAbstractCutterDesign',)


class CylindricalGearAbstractCutterDesign(_1605.NamedDatabaseItem):
    """CylindricalGearAbstractCutterDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_ABSTRACT_CUTTER_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearAbstractCutterDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cutter_type(self) -> 'str':
        """str: 'CutterType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterType

        if temp is None:
            return None

        return temp

    @property
    def edge_radius(self) -> 'float':
        """float: 'EdgeRadius' is the original name of this property."""

        temp = self.wrapped.EdgeRadius

        if temp is None:
            return None

        return temp

    @edge_radius.setter
    def edge_radius(self, value: 'float'):
        self.wrapped.EdgeRadius = float(value) if value else 0.0

    @property
    def nominal_normal_pressure_angle(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NominalNormalPressureAngle' is the original name of this property."""

        temp = self.wrapped.NominalNormalPressureAngle

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @nominal_normal_pressure_angle.setter
    def nominal_normal_pressure_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NominalNormalPressureAngle = value

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
