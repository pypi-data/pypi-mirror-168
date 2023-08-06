"""_2133.py

FESubstructure
"""


from typing import List, Optional

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.system_model.fe import (
    _2107, _2113, _2161, _2138,
    _2109, _2134, _2145, _2131,
    _2146, _2135, _2159, _2141,
    _2142, _2143, _2144
)
from mastapy._internal.implicit import list_with_selected_item, overridable, enum_with_selected_value
from mastapy.system_model.part_model import _2195, _2199, _2203
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility.units_and_measurements import _1411
from mastapy._internal.python_net import python_net_import
from mastapy.nodal_analysis import (
    _67, _81, _57, _63
)
from mastapy.materials import _215, _257
from mastapy.system_model import _1974
from mastapy.nodal_analysis.component_mode_synthesis import _205
from mastapy.math_utility import _1305
from mastapy.nodal_analysis.geometry_modeller_link import _151
from mastapy.system_model.fe.links import _2168
from mastapy.system_model.part_model.shaft_model import _2232
from mastapy.math_utility.measured_vectors import _1371
from mastapy.nodal_analysis.fe_export_utility import _158
from mastapy import _7285

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_STRING = python_net_import('System', 'String')
_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_FE_SUBSTRUCTURE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructure')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructure',)


class FESubstructure(_63.FEStiffness):
    """FESubstructure

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE

    def __init__(self, instance_to_wrap: 'FESubstructure.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def actual_number_of_rigid_body_modes(self) -> 'int':
        """int: 'ActualNumberOfRigidBodyModes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualNumberOfRigidBodyModes

        if temp is None:
            return None

        return temp

    @property
    def alignment_method(self) -> '_2107.AlignmentMethod':
        """AlignmentMethod: 'AlignmentMethod' is the original name of this property."""

        temp = self.wrapped.AlignmentMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2107.AlignmentMethod)(value) if value is not None else None

    @alignment_method.setter
    def alignment_method(self, value: '_2107.AlignmentMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AlignmentMethod = value

    @property
    def angle_span(self) -> 'float':
        """float: 'AngleSpan' is the original name of this property."""

        temp = self.wrapped.AngleSpan

        if temp is None:
            return None

        return temp

    @angle_span.setter
    def angle_span(self, value: 'float'):
        self.wrapped.AngleSpan = float(value) if value else 0.0

    @property
    def angular_alignment_tolerance(self) -> 'float':
        """float: 'AngularAlignmentTolerance' is the original name of this property."""

        temp = self.wrapped.AngularAlignmentTolerance

        if temp is None:
            return None

        return temp

    @angular_alignment_tolerance.setter
    def angular_alignment_tolerance(self, value: 'float'):
        self.wrapped.AngularAlignmentTolerance = float(value) if value else 0.0

    @property
    def apply_translation_and_rotation_for_planetary_duplicates(self) -> 'bool':
        """bool: 'ApplyTranslationAndRotationForPlanetaryDuplicates' is the original name of this property."""

        temp = self.wrapped.ApplyTranslationAndRotationForPlanetaryDuplicates

        if temp is None:
            return None

        return temp

    @apply_translation_and_rotation_for_planetary_duplicates.setter
    def apply_translation_and_rotation_for_planetary_duplicates(self, value: 'bool'):
        self.wrapped.ApplyTranslationAndRotationForPlanetaryDuplicates = bool(value) if value else False

    @property
    def are_vectors_loaded(self) -> 'bool':
        """bool: 'AreVectorsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreVectorsLoaded

        if temp is None:
            return None

        return temp

    @property
    def bearing_node_alignment(self) -> '_2113.BearingNodeAlignmentOption':
        """BearingNodeAlignmentOption: 'BearingNodeAlignment' is the original name of this property."""

        temp = self.wrapped.BearingNodeAlignment

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2113.BearingNodeAlignmentOption)(value) if value is not None else None

    @bearing_node_alignment.setter
    def bearing_node_alignment(self, value: '_2113.BearingNodeAlignmentOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingNodeAlignment = value

    @property
    def bearing_races_in_fe(self) -> 'bool':
        """bool: 'BearingRacesInFE' is the original name of this property."""

        temp = self.wrapped.BearingRacesInFE

        if temp is None:
            return None

        return temp

    @bearing_races_in_fe.setter
    def bearing_races_in_fe(self, value: 'bool'):
        self.wrapped.BearingRacesInFE = bool(value) if value else False

    @property
    def check_fe_has_internal_modes_before_nvh_analysis(self) -> 'bool':
        """bool: 'CheckFEHasInternalModesBeforeNVHAnalysis' is the original name of this property."""

        temp = self.wrapped.CheckFEHasInternalModesBeforeNVHAnalysis

        if temp is None:
            return None

        return temp

    @check_fe_has_internal_modes_before_nvh_analysis.setter
    def check_fe_has_internal_modes_before_nvh_analysis(self, value: 'bool'):
        self.wrapped.CheckFEHasInternalModesBeforeNVHAnalysis = bool(value) if value else False

    @property
    def comment(self) -> 'str':
        """str: 'Comment' is the original name of this property."""

        temp = self.wrapped.Comment

        if temp is None:
            return None

        return temp

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value else ''

    @property
    def component_to_align_to(self) -> 'list_with_selected_item.ListWithSelectedItem_Component':
        """list_with_selected_item.ListWithSelectedItem_Component: 'ComponentToAlignTo' is the original name of this property."""

        temp = self.wrapped.ComponentToAlignTo

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Component)(temp) if temp is not None else None

    @component_to_align_to.setter
    def component_to_align_to(self, value: 'list_with_selected_item.ListWithSelectedItem_Component.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Component.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Component.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ComponentToAlignTo = value

    @property
    def condensation_node_size(self) -> 'float':
        """float: 'CondensationNodeSize' is the original name of this property."""

        temp = self.wrapped.CondensationNodeSize

        if temp is None:
            return None

        return temp

    @condensation_node_size.setter
    def condensation_node_size(self, value: 'float'):
        self.wrapped.CondensationNodeSize = float(value) if value else 0.0

    @property
    def datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        """list_with_selected_item.ListWithSelectedItem_Datum: 'Datum' is the original name of this property."""

        temp = self.wrapped.Datum

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Datum)(temp) if temp is not None else None

    @datum.setter
    def datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.Datum = value

    @property
    def distance_display_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'DistanceDisplayUnit' is the original name of this property."""

        temp = self.wrapped.DistanceDisplayUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @distance_display_unit.setter
    def distance_display_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.DistanceDisplayUnit = value

    @property
    def expected_number_of_rigid_body_modes(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'ExpectedNumberOfRigidBodyModes' is the original name of this property."""

        temp = self.wrapped.ExpectedNumberOfRigidBodyModes

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @expected_number_of_rigid_body_modes.setter
    def expected_number_of_rigid_body_modes(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.ExpectedNumberOfRigidBodyModes = value

    @property
    def external_fe_forces_are_from_gravity_only(self) -> 'bool':
        """bool: 'ExternalFEForcesAreFromGravityOnly' is the original name of this property."""

        temp = self.wrapped.ExternalFEForcesAreFromGravityOnly

        if temp is None:
            return None

        return temp

    @external_fe_forces_are_from_gravity_only.setter
    def external_fe_forces_are_from_gravity_only(self, value: 'bool'):
        self.wrapped.ExternalFEForcesAreFromGravityOnly = bool(value) if value else False

    @property
    def force_display_unit(self) -> 'list_with_selected_item.ListWithSelectedItem_Unit':
        """list_with_selected_item.ListWithSelectedItem_Unit: 'ForceDisplayUnit' is the original name of this property."""

        temp = self.wrapped.ForceDisplayUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_Unit)(temp) if temp is not None else None

    @force_display_unit.setter
    def force_display_unit(self, value: 'list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ForceDisplayUnit = value

    @property
    def full_fe_model_mesh_path(self) -> 'str':
        """str: 'FullFEModelMeshPath' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEModelMeshPath

        if temp is None:
            return None

        return temp

    @property
    def full_fe_model_mesh_size(self) -> 'str':
        """str: 'FullFEModelMeshSize' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEModelMeshSize

        if temp is None:
            return None

        return temp

    @property
    def full_fe_model_vectors_path(self) -> 'str':
        """str: 'FullFEModelVectorsPath' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEModelVectorsPath

        if temp is None:
            return None

        return temp

    @property
    def full_fe_model_vectors_size(self) -> 'str':
        """str: 'FullFEModelVectorsSize' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FullFEModelVectorsSize

        if temp is None:
            return None

        return temp

    @property
    def geometry_meshing_material(self) -> 'str':
        """str: 'GeometryMeshingMaterial' is the original name of this property."""

        temp = self.wrapped.GeometryMeshingMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @geometry_meshing_material.setter
    def geometry_meshing_material(self, value: 'str'):
        self.wrapped.GeometryMeshingMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def gravity_force_can_be_rotated(self) -> 'bool':
        """bool: 'GravityForceCanBeRotated' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GravityForceCanBeRotated

        if temp is None:
            return None

        return temp

    @property
    def gravity_force_source(self) -> '_67.GravityForceSource':
        """GravityForceSource: 'GravityForceSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GravityForceSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_67.GravityForceSource)(value) if value is not None else None

    @property
    def gravity_magnitude_used_for_reduced_forces(self) -> 'float':
        """float: 'GravityMagnitudeUsedForReducedForces' is the original name of this property."""

        temp = self.wrapped.GravityMagnitudeUsedForReducedForces

        if temp is None:
            return None

        return temp

    @gravity_magnitude_used_for_reduced_forces.setter
    def gravity_magnitude_used_for_reduced_forces(self, value: 'float'):
        self.wrapped.GravityMagnitudeUsedForReducedForces = float(value) if value else 0.0

    @property
    def housing_is_grounded(self) -> 'bool':
        """bool: 'HousingIsGrounded' is the original name of this property."""

        temp = self.wrapped.HousingIsGrounded

        if temp is None:
            return None

        return temp

    @housing_is_grounded.setter
    def housing_is_grounded(self, value: 'bool'):
        self.wrapped.HousingIsGrounded = bool(value) if value else False

    @property
    def is_housing(self) -> 'bool':
        """bool: 'IsHousing' is the original name of this property."""

        temp = self.wrapped.IsHousing

        if temp is None:
            return None

        return temp

    @is_housing.setter
    def is_housing(self, value: 'bool'):
        self.wrapped.IsHousing = bool(value) if value else False

    @property
    def is_mesh_loaded(self) -> 'bool':
        """bool: 'IsMeshLoaded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsMeshLoaded

        if temp is None:
            return None

        return temp

    @property
    def material(self) -> 'str':
        """str: 'Material' is the original name of this property."""

        temp = self.wrapped.Material.SelectedItemName

        if temp is None:
            return None

        return temp

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else '')

    @property
    def non_condensation_node_size(self) -> 'int':
        """int: 'NonCondensationNodeSize' is the original name of this property."""

        temp = self.wrapped.NonCondensationNodeSize

        if temp is None:
            return None

        return temp

    @non_condensation_node_size.setter
    def non_condensation_node_size(self, value: 'int'):
        self.wrapped.NonCondensationNodeSize = int(value) if value else 0

    @property
    def number_of_angles(self) -> 'int':
        """int: 'NumberOfAngles' is the original name of this property."""

        temp = self.wrapped.NumberOfAngles

        if temp is None:
            return None

        return temp

    @number_of_angles.setter
    def number_of_angles(self, value: 'int'):
        self.wrapped.NumberOfAngles = int(value) if value else 0

    @property
    def number_of_condensation_nodes(self) -> 'int':
        """int: 'NumberOfCondensationNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfCondensationNodes

        if temp is None:
            return None

        return temp

    @property
    def number_of_condensation_nodes_in_reduced_model(self) -> 'int':
        """int: 'NumberOfCondensationNodesInReducedModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfCondensationNodesInReducedModel

        if temp is None:
            return None

        return temp

    @property
    def polar_inertia(self) -> 'float':
        """float: 'PolarInertia' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PolarInertia

        if temp is None:
            return None

        return temp

    @property
    def reduced_stiffness_file(self) -> 'str':
        """str: 'ReducedStiffnessFile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReducedStiffnessFile

        if temp is None:
            return None

        return temp

    @property
    def reduced_stiffness_file_editable(self) -> 'str':
        """str: 'ReducedStiffnessFileEditable' is the original name of this property."""

        temp = self.wrapped.ReducedStiffnessFileEditable

        if temp is None:
            return None

        return temp

    @reduced_stiffness_file_editable.setter
    def reduced_stiffness_file_editable(self, value: 'str'):
        self.wrapped.ReducedStiffnessFileEditable = str(value) if value else ''

    @property
    def thermal_expansion_option(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption':
        """enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption: 'ThermalExpansionOption' is the original name of this property."""

        temp = self.wrapped.ThermalExpansionOption

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @thermal_expansion_option.setter
    def thermal_expansion_option(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ThermalExpansionOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ThermalExpansionOption = value

    @property
    def torque_transmission_relative_tolerance(self) -> 'float':
        """float: 'TorqueTransmissionRelativeTolerance' is the original name of this property."""

        temp = self.wrapped.TorqueTransmissionRelativeTolerance

        if temp is None:
            return None

        return temp

    @torque_transmission_relative_tolerance.setter
    def torque_transmission_relative_tolerance(self, value: 'float'):
        self.wrapped.TorqueTransmissionRelativeTolerance = float(value) if value else 0.0

    @property
    def type_(self) -> 'enum_with_selected_value.EnumWithSelectedValue_FESubstructureType':
        """enum_with_selected_value.EnumWithSelectedValue_FESubstructureType: 'Type' is the original name of this property."""

        temp = self.wrapped.Type

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @type_.setter
    def type_(self, value: 'enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FESubstructureType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.Type = value

    @property
    def acoustic_radiation_efficiency(self) -> '_215.AcousticRadiationEfficiency':
        """AcousticRadiationEfficiency: 'AcousticRadiationEfficiency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AcousticRadiationEfficiency

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def alignment_using_axial_node_positions(self) -> '_2109.AlignmentUsingAxialNodePositions':
        """AlignmentUsingAxialNodePositions: 'AlignmentUsingAxialNodePositions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AlignmentUsingAxialNodePositions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def alignment_to_component(self) -> '_1974.RelativeComponentAlignment[_2195.Component]':
        """RelativeComponentAlignment[Component]: 'AlignmentToComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AlignmentToComponent

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_2195.Component](temp) if temp is not None else None

    @property
    def cms_model(self) -> '_205.CMSModel':
        """CMSModel: 'CMSModel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CMSModel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def coordinate_system(self) -> '_1305.CoordinateSystem3D':
        """CoordinateSystem3D: 'CoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoordinateSystem

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def export(self) -> '_2134.FESubstructureExportOptions':
        """FESubstructureExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Export

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def fe_meshing_options(self) -> '_81.ShaftFEMeshingOptions':
        """ShaftFEMeshingOptions: 'FEMeshingOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEMeshingOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def geometry_modeller_dimensions(self) -> '_151.GeometryModellerDimensions':
        """GeometryModellerDimensions: 'GeometryModellerDimensions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryModellerDimensions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sound_pressure_enclosure(self) -> '_257.SoundPressureEnclosure':
        """SoundPressureEnclosure: 'SoundPressureEnclosure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SoundPressureEnclosure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_meshing_options(self) -> 'List[_2145.GearMeshingOptions]':
        """List[GearMeshingOptions]: 'GearMeshingOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMeshingOptions

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def geometries(self) -> 'List[_2131.FEStiffnessGeometry]':
        """List[FEStiffnessGeometry]: 'Geometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Geometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def independent_masta_created_condensation_nodes(self) -> 'List[_2146.IndependentMastaCreatedCondensationNode]':
        """List[IndependentMastaCreatedCondensationNode]: 'IndependentMastaCreatedCondensationNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IndependentMastaCreatedCondensationNodes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def links(self) -> 'List[_2168.FELink]':
        """List[FELink]: 'Links' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Links

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def nodes(self) -> 'List[_2135.FESubstructureNode]':
        """List[FESubstructureNode]: 'Nodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Nodes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def replaced_shafts(self) -> 'List[_2232.Shaft]':
        """List[Shaft]: 'ReplacedShafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReplacedShafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts_that_can_be_replaced(self) -> 'List[_2159.ReplacedShaftSelectionHelper]':
        """List[ReplacedShaftSelectionHelper]: 'ShaftsThatCanBeReplaced' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftsThatCanBeReplaced

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def thermal_expansion_displacements(self) -> 'List[_1371.VectorWithLinearAndAngularComponents]':
        """List[VectorWithLinearAndAngularComponents]: 'ThermalExpansionDisplacements' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalExpansionDisplacements

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def thermal_expansion_forces(self) -> 'List[_1371.VectorWithLinearAndAngularComponents]':
        """List[VectorWithLinearAndAngularComponents]: 'ThermalExpansionForces' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalExpansionForces

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_part(self) -> '_2203.FEPart':
        """FEPart: 'FEPart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEPart

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else ''

    def add_geometry(self):
        """ 'AddGeometry' is the original name of this method."""

        self.wrapped.AddGeometry()

    def auto_connect_external_nodes(self):
        """ 'AutoConnectExternalNodes' is the original name of this method."""

        self.wrapped.AutoConnectExternalNodes()

    def copy_datum_to_manual(self):
        """ 'CopyDatumToManual' is the original name of this method."""

        self.wrapped.CopyDatumToManual()

    def create_datum_from_manual_alignment(self):
        """ 'CreateDatumFromManualAlignment' is the original name of this method."""

        self.wrapped.CreateDatumFromManualAlignment()

    def create_fe_volume_mesh(self):
        """ 'CreateFEVolumeMesh' is the original name of this method."""

        self.wrapped.CreateFEVolumeMesh()

    def default_node_creation_options(self):
        """ 'DefaultNodeCreationOptions' is the original name of this method."""

        self.wrapped.DefaultNodeCreationOptions()

    def delete_all_links(self):
        """ 'DeleteAllLinks' is the original name of this method."""

        self.wrapped.DeleteAllLinks()

    def embed_fe_model_mesh_in_masta_file(self):
        """ 'EmbedFEModelMeshInMASTAFile' is the original name of this method."""

        self.wrapped.EmbedFEModelMeshInMASTAFile()

    def embed_fe_model_vectors_in_masta_file(self):
        """ 'EmbedFEModelVectorsInMASTAFile' is the original name of this method."""

        self.wrapped.EmbedFEModelVectorsInMASTAFile()

    def perform_reduction(self):
        """ 'PerformReduction' is the original name of this method."""

        self.wrapped.PerformReduction()

    def re_import_external_fe_mesh(self):
        """ 'ReImportExternalFEMesh' is the original name of this method."""

        self.wrapped.ReImportExternalFEMesh()

    def remove_full_fe_mesh(self):
        """ 'RemoveFullFEMesh' is the original name of this method."""

        self.wrapped.RemoveFullFEMesh()

    def reread_mesh_from_geometry_modeller(self):
        """ 'RereadMeshFromGeometryModeller' is the original name of this method."""

        self.wrapped.RereadMeshFromGeometryModeller()

    def unload_external_mesh_file(self):
        """ 'UnloadExternalMeshFile' is the original name of this method."""

        self.wrapped.UnloadExternalMeshFile()

    def unload_external_vectors_file(self):
        """ 'UnloadExternalVectorsFile' is the original name of this method."""

        self.wrapped.UnloadExternalVectorsFile()

    def update_gear_teeth_mesh(self):
        """ 'UpdateGearTeethMesh' is the original name of this method."""

        self.wrapped.UpdateGearTeethMesh()

    def convert_shafts_to_fe(self, operation: '_57.FEMeshingOperation', export_file_name: 'str'):
        """ 'ConvertShaftsToFE' is the original name of this method.

        Args:
            operation (mastapy.nodal_analysis.FEMeshingOperation)
            export_file_name (str)
        """

        operation = conversion.mp_to_pn_enum(operation)
        export_file_name = str(export_file_name)
        self.wrapped.ConvertShaftsToFE(operation, export_file_name if export_file_name else '')

    def create_fe_substructure_with_selection_components(self) -> '_2141.FESubstructureWithSelectionComponents':
        """ 'CreateFESubstructureWithSelectionComponents' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionComponents
        """

        method_result = self.wrapped.CreateFESubstructureWithSelectionComponents()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_fe_substructure_with_selection_for_harmonic_analysis(self) -> '_2142.FESubstructureWithSelectionForHarmonicAnalysis':
        """ 'CreateFESubstructureWithSelectionForHarmonicAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForHarmonicAnalysis
        """

        method_result = self.wrapped.CreateFESubstructureWithSelectionForHarmonicAnalysis()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_fe_substructure_with_selection_for_modal_analysis(self) -> '_2143.FESubstructureWithSelectionForModalAnalysis':
        """ 'CreateFESubstructureWithSelectionForModalAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForModalAnalysis
        """

        method_result = self.wrapped.CreateFESubstructureWithSelectionForModalAnalysis()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_fe_substructure_with_selection_for_static_analysis(self) -> '_2144.FESubstructureWithSelectionForStaticAnalysis':
        """ 'CreateFESubstructureWithSelectionForStaticAnalysis' is the original name of this method.

        Returns:
            mastapy.system_model.fe.FESubstructureWithSelectionForStaticAnalysis
        """

        method_result = self.wrapped.CreateFESubstructureWithSelectionForStaticAnalysis()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def duplicate(self, name: 'str') -> 'FESubstructure':
        """ 'Duplicate' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.fe.FESubstructure
        """

        name = str(name)
        method_result = self.wrapped.Duplicate(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def import_fe_mesh(self, file_path: 'str', format_: '_158.FEExportFormat', length_scale: Optional['float'] = 1.0, force_scale: Optional['float'] = 1.0, progress: Optional['_7285.TaskProgress'] = None):
        """ 'ImportFEMesh' is the original name of this method.

        Args:
            file_path (str)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
            progress (mastapy.TaskProgress, optional)
        """

        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(format_)
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        self.wrapped.ImportFEMesh(file_path if file_path else '', format_, length_scale if length_scale else 0.0, force_scale if force_scale else 0.0, progress.wrapped if progress else None)

    def import_node_positions(self, file_name: 'str', distance_unit: '_1411.Unit'):
        """ 'ImportNodePositions' is the original name of this method.

        Args:
            file_name (str)
            distance_unit (mastapy.utility.units_and_measurements.Unit)
        """

        file_name = str(file_name)
        self.wrapped.ImportNodePositions(file_name if file_name else '', distance_unit.wrapped if distance_unit else None)

    def import_reduced_stiffness(self, file_name: 'str', distance_unit: '_1411.Unit', force_unit: '_1411.Unit'):
        """ 'ImportReducedStiffness' is the original name of this method.

        Args:
            file_name (str)
            distance_unit (mastapy.utility.units_and_measurements.Unit)
            force_unit (mastapy.utility.units_and_measurements.Unit)
        """

        file_name = str(file_name)
        self.wrapped.ImportReducedStiffness(file_name if file_name else '', distance_unit.wrapped if distance_unit else None, force_unit.wrapped if force_unit else None)

    def links_for(self, node: '_2135.FESubstructureNode') -> 'List[_2168.FELink]':
        """ 'LinksFor' is the original name of this method.

        Args:
            node (mastapy.system_model.fe.FESubstructureNode)

        Returns:
            List[mastapy.system_model.fe.links.FELink]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.LinksFor(node.wrapped if node else None))

    def load_existing_masta_fe_file(self, file_name: 'str'):
        """ 'LoadExistingMastaFEFile' is the original name of this method.

        Args:
            file_name (str)
        """

        file_name = str(file_name)
        self.wrapped.LoadExistingMastaFEFile.Overloads[_STRING](file_name if file_name else '')

    def load_existing_masta_fe_file_with_progress(self, file_name: 'str', progress: '_7285.TaskProgress'):
        """ 'LoadExistingMastaFEFile' is the original name of this method.

        Args:
            file_name (str)
            progress (mastapy.TaskProgress)
        """

        file_name = str(file_name)
        self.wrapped.LoadExistingMastaFEFile.Overloads[_STRING, _TASK_PROGRESS](file_name if file_name else '', progress.wrapped if progress else None)

    def load_external_mesh(self, file_path: 'str'):
        """ 'LoadExternalMesh' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.LoadExternalMesh(file_path if file_path else '')

    def load_external_vectors(self, file_path: 'str'):
        """ 'LoadExternalVectors' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.LoadExternalVectors(file_path if file_path else '')

    def load_stl_geometry(self, length_unit: '_1411.Unit', file_name: 'str'):
        """ 'LoadStlGeometry' is the original name of this method.

        Args:
            length_unit (mastapy.utility.units_and_measurements.Unit)
            file_name (str)
        """

        file_name = str(file_name)
        self.wrapped.LoadStlGeometry(length_unit.wrapped if length_unit else None, file_name if file_name else '')

    def store_full_fe_mesh_in_external_file(self, external_fe_path: 'str'):
        """ 'StoreFullFeMeshInExternalFile' is the original name of this method.

        Args:
            external_fe_path (str)
        """

        external_fe_path = str(external_fe_path)
        self.wrapped.StoreFullFeMeshInExternalFile(external_fe_path if external_fe_path else '')

    def store_full_fe_model_vectors_in_external_file(self, external_fe_path: 'str'):
        """ 'StoreFullFeModelVectorsInExternalFile' is the original name of this method.

        Args:
            external_fe_path (str)
        """

        external_fe_path = str(external_fe_path)
        self.wrapped.StoreFullFeModelVectorsInExternalFile(external_fe_path if external_fe_path else '')
