"""_850.py

CylindricalMeshLoadCase
"""


from mastapy.gears import _295, _296
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _1020
from mastapy.gears.load_case import _841
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Cylindrical', 'CylindricalMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalMeshLoadCase',)


class CylindricalMeshLoadCase(_841.MeshLoadCase):
    """CylindricalMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MESH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'CylindricalMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_295.CylindricalFlanks':
        """CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_295.CylindricalFlanks)(value) if value is not None else None

    @property
    def equivalent_misalignment(self) -> 'float':
        """float: 'EquivalentMisalignment' is the original name of this property."""

        temp = self.wrapped.EquivalentMisalignment

        if temp is None:
            return None

        return temp

    @equivalent_misalignment.setter
    def equivalent_misalignment(self, value: 'float'):
        self.wrapped.EquivalentMisalignment = float(value) if value else 0.0

    @property
    def equivalent_misalignment_due_to_system_deflection(self) -> 'float':
        """float: 'EquivalentMisalignmentDueToSystemDeflection' is the original name of this property."""

        temp = self.wrapped.EquivalentMisalignmentDueToSystemDeflection

        if temp is None:
            return None

        return temp

    @equivalent_misalignment_due_to_system_deflection.setter
    def equivalent_misalignment_due_to_system_deflection(self, value: 'float'):
        self.wrapped.EquivalentMisalignmentDueToSystemDeflection = float(value) if value else 0.0

    @property
    def misalignment_source(self) -> '_296.CylindricalMisalignmentDataSource':
        """CylindricalMisalignmentDataSource: 'MisalignmentSource' is the original name of this property."""

        temp = self.wrapped.MisalignmentSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_296.CylindricalMisalignmentDataSource)(value) if value is not None else None

    @misalignment_source.setter
    def misalignment_source(self, value: '_296.CylindricalMisalignmentDataSource'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MisalignmentSource = value

    @property
    def misalignment_due_to_micro_geometry_lead_relief(self) -> 'float':
        """float: 'MisalignmentDueToMicroGeometryLeadRelief' is the original name of this property."""

        temp = self.wrapped.MisalignmentDueToMicroGeometryLeadRelief

        if temp is None:
            return None

        return temp

    @misalignment_due_to_micro_geometry_lead_relief.setter
    def misalignment_due_to_micro_geometry_lead_relief(self, value: 'float'):
        self.wrapped.MisalignmentDueToMicroGeometryLeadRelief = float(value) if value else 0.0

    @property
    def pitch_line_velocity_at_operating_pitch_diameter(self) -> 'float':
        """float: 'PitchLineVelocityAtOperatingPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchLineVelocityAtOperatingPitchDiameter

        if temp is None:
            return None

        return temp

    @property
    def load_case_modifiable_settings(self) -> '_1020.LTCALoadCaseModifiableSettings':
        """LTCALoadCaseModifiableSettings: 'LoadCaseModifiableSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCaseModifiableSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
