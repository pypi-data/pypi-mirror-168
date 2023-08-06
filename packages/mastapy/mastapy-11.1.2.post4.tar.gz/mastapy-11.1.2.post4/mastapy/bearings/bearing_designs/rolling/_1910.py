"""_1910.py

FourPointContactBallBearing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.bearings.bearing_designs.rolling import _1909, _1915
from mastapy._internal.python_net import python_net_import

_FOUR_POINT_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'FourPointContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('FourPointContactBallBearing',)


class FourPointContactBallBearing(_1915.MultiPointContactBallBearing):
    """FourPointContactBallBearing

    This is a mastapy class.
    """

    TYPE = _FOUR_POINT_CONTACT_BALL_BEARING

    def __init__(self, instance_to_wrap: 'FourPointContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_axial_internal_clearance(self) -> 'float':
        """float: 'AssemblyAxialInternalClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAxialInternalClearance

        if temp is None:
            return None

        return temp

    @property
    def contact_angle_under_axial_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ContactAngleUnderAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleUnderAxialLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def contact_angle_under_radial_load(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ContactAngleUnderRadialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleUnderRadialLoad

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @property
    def contact_angle_and_internal_clearance_definition(self) -> '_1909.FourPointContactAngleDefinition':
        """FourPointContactAngleDefinition: 'ContactAngleAndInternalClearanceDefinition' is the original name of this property."""

        temp = self.wrapped.ContactAngleAndInternalClearanceDefinition

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1909.FourPointContactAngleDefinition)(value) if value is not None else None

    @contact_angle_and_internal_clearance_definition.setter
    def contact_angle_and_internal_clearance_definition(self, value: '_1909.FourPointContactAngleDefinition'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ContactAngleAndInternalClearanceDefinition = value

    @property
    def nominal_radial_internal_clearance(self) -> 'float':
        """float: 'NominalRadialInternalClearance' is the original name of this property."""

        temp = self.wrapped.NominalRadialInternalClearance

        if temp is None:
            return None

        return temp

    @nominal_radial_internal_clearance.setter
    def nominal_radial_internal_clearance(self, value: 'float'):
        self.wrapped.NominalRadialInternalClearance = float(value) if value else 0.0
