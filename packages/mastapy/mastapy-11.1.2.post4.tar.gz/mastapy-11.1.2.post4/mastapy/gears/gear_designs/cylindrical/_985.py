"""_985.py

CylindricalGearPinionTypeCutter
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.cylindrical import _986, _969
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_PINION_TYPE_CUTTER = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearPinionTypeCutter')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearPinionTypeCutter',)


class CylindricalGearPinionTypeCutter(_969.CylindricalGearAbstractRack):
    """CylindricalGearPinionTypeCutter

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_PINION_TYPE_CUTTER

    def __init__(self, instance_to_wrap: 'CylindricalGearPinionTypeCutter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def nominal_addendum_factor(self) -> 'float':
        """float: 'NominalAddendumFactor' is the original name of this property."""

        temp = self.wrapped.NominalAddendumFactor

        if temp is None:
            return None

        return temp

    @nominal_addendum_factor.setter
    def nominal_addendum_factor(self, value: 'float'):
        self.wrapped.NominalAddendumFactor = float(value) if value else 0.0

    @property
    def nominal_dedendum_factor(self) -> 'float':
        """float: 'NominalDedendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalDedendumFactor

        if temp is None:
            return None

        return temp

    @property
    def number_of_teeth(self) -> 'int':
        """int: 'NumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.NumberOfTeeth

        if temp is None:
            return None

        return temp

    @number_of_teeth.setter
    def number_of_teeth(self, value: 'int'):
        self.wrapped.NumberOfTeeth = int(value) if value else 0

    @property
    def profile_shift_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ProfileShiftCoefficient' is the original name of this property."""

        temp = self.wrapped.ProfileShiftCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @profile_shift_coefficient.setter
    def profile_shift_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ProfileShiftCoefficient = value

    @property
    def left_flank(self) -> '_986.CylindricalGearPinionTypeCutterFlank':
        """CylindricalGearPinionTypeCutterFlank: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_986.CylindricalGearPinionTypeCutterFlank':
        """CylindricalGearPinionTypeCutterFlank: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
