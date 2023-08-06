"""_1283.py

DetailedBoltDesign
"""


from typing import List

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy.bolts import (
    _1281, _1286, _1289, _1274,
    _1276, _1272
)
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import
from mastapy._internal.cast_exception import CastException
from mastapy._math.vector_3d import Vector3D
from mastapy import _0

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_DETAILED_BOLT_DESIGN = python_net_import('SMT.MastaAPI.Bolts', 'DetailedBoltDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('DetailedBoltDesign',)


class DetailedBoltDesign(_0.APIBase):
    """DetailedBoltDesign

    This is a mastapy class.
    """

    TYPE = _DETAILED_BOLT_DESIGN

    def __init__(self, instance_to_wrap: 'DetailedBoltDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def appropriate_minimum_bolt_diameter(self) -> 'float':
        """float: 'AppropriateMinimumBoltDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AppropriateMinimumBoltDiameter

        if temp is None:
            return None

        return temp

    @property
    def appropriate_minimum_cross_sectional_area_for_hollow_bolt(self) -> 'float':
        """float: 'AppropriateMinimumCrossSectionalAreaForHollowBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AppropriateMinimumCrossSectionalAreaForHollowBolt

        if temp is None:
            return None

        return temp

    @property
    def average_outside_diameter_of_clamped_parts(self) -> 'float':
        """float: 'AverageOutsideDiameterOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageOutsideDiameterOfClampedParts

        if temp is None:
            return None

        return temp

    @property
    def average_surface_roughness(self) -> 'float':
        """float: 'AverageSurfaceRoughness' is the original name of this property."""

        temp = self.wrapped.AverageSurfaceRoughness

        if temp is None:
            return None

        return temp

    @average_surface_roughness.setter
    def average_surface_roughness(self, value: 'float'):
        self.wrapped.AverageSurfaceRoughness = float(value) if value else 0.0

    @property
    def bearing_area_diameter_at_the_interface(self) -> 'float':
        """float: 'BearingAreaDiameterAtTheInterface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingAreaDiameterAtTheInterface

        if temp is None:
            return None

        return temp

    @property
    def chamfer_diameter_at_the_clamped_parts(self) -> 'float':
        """float: 'ChamferDiameterAtTheClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ChamferDiameterAtTheClampedParts

        if temp is None:
            return None

        return temp

    @property
    def clamped_parts(self) -> 'List[_1281.ClampedSection]':
        """List[ClampedSection]: 'ClampedParts' is the original name of this property."""

        temp = self.wrapped.ClampedParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @clamped_parts.setter
    def clamped_parts(self, value: 'List[_1281.ClampedSection]'):
        value = value if value else None
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.ClampedParts = value

    @property
    def clamping_length(self) -> 'float':
        """float: 'ClampingLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClampingLength

        if temp is None:
            return None

        return temp

    @property
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(self) -> 'bool':
        """bool: 'ConsiderThisTappedThreadBoltAsAThroughBoltedJoint' is the original name of this property."""

        temp = self.wrapped.ConsiderThisTappedThreadBoltAsAThroughBoltedJoint

        if temp is None:
            return None

        return temp

    @consider_this_tapped_thread_bolt_as_a_through_bolted_joint.setter
    def consider_this_tapped_thread_bolt_as_a_through_bolted_joint(self, value: 'bool'):
        self.wrapped.ConsiderThisTappedThreadBoltAsAThroughBoltedJoint = bool(value) if value else False

    @property
    def counter_bore_depth(self) -> 'float':
        """float: 'CounterBoreDepth' is the original name of this property."""

        temp = self.wrapped.CounterBoreDepth

        if temp is None:
            return None

        return temp

    @counter_bore_depth.setter
    def counter_bore_depth(self, value: 'float'):
        self.wrapped.CounterBoreDepth = float(value) if value else 0.0

    @property
    def cross_section_of_thread(self) -> 'float':
        """float: 'CrossSectionOfThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrossSectionOfThread

        if temp is None:
            return None

        return temp

    @property
    def deformation_cone_angle(self) -> 'float':
        """float: 'DeformationConeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeformationConeAngle

        if temp is None:
            return None

        return temp

    @property
    def diameter_ratio(self) -> 'float':
        """float: 'DiameterRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterRatio

        if temp is None:
            return None

        return temp

    @property
    def diameter_for_the_specified_standard_size(self) -> 'float':
        """float: 'DiameterForTheSpecifiedStandardSize' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterForTheSpecifiedStandardSize

        if temp is None:
            return None

        return temp

    @property
    def diameter_of_shearing_cross_section(self) -> 'float':
        """float: 'DiameterOfShearingCrossSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiameterOfShearingCrossSection

        if temp is None:
            return None

        return temp

    @property
    def distance_of_bolt_axis_from_central_point(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'DistanceOfBoltAxisFromCentralPoint' is the original name of this property."""

        temp = self.wrapped.DistanceOfBoltAxisFromCentralPoint

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @distance_of_bolt_axis_from_central_point.setter
    def distance_of_bolt_axis_from_central_point(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.DistanceOfBoltAxisFromCentralPoint = value

    @property
    def distance_of_the_bolt_axis_from_edge_of_interface(self) -> 'float':
        """float: 'DistanceOfTheBoltAxisFromEdgeOfInterface' is the original name of this property."""

        temp = self.wrapped.DistanceOfTheBoltAxisFromEdgeOfInterface

        if temp is None:
            return None

        return temp

    @distance_of_the_bolt_axis_from_edge_of_interface.setter
    def distance_of_the_bolt_axis_from_edge_of_interface(self, value: 'float'):
        self.wrapped.DistanceOfTheBoltAxisFromEdgeOfInterface = float(value) if value else 0.0

    @property
    def edit_bolt_geometry(self) -> 'str':
        """str: 'EditBoltGeometry' is the original name of this property."""

        temp = self.wrapped.EditBoltGeometry.SelectedItemName

        if temp is None:
            return None

        return temp

    @edit_bolt_geometry.setter
    def edit_bolt_geometry(self, value: 'str'):
        self.wrapped.EditBoltGeometry.SetSelectedItem(str(value) if value else '')

    @property
    def edit_bolt_material(self) -> 'str':
        """str: 'EditBoltMaterial' is the original name of this property."""

        temp = self.wrapped.EditBoltMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @edit_bolt_material.setter
    def edit_bolt_material(self, value: 'str'):
        self.wrapped.EditBoltMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def edit_nut_material(self) -> 'str':
        """str: 'EditNutMaterial' is the original name of this property."""

        temp = self.wrapped.EditNutMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @edit_nut_material.setter
    def edit_nut_material(self, value: 'str'):
        self.wrapped.EditNutMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def edit_tapped_thread_material(self) -> 'str':
        """str: 'EditTappedThreadMaterial' is the original name of this property."""

        temp = self.wrapped.EditTappedThreadMaterial.SelectedItemName

        if temp is None:
            return None

        return temp

    @edit_tapped_thread_material.setter
    def edit_tapped_thread_material(self, value: 'str'):
        self.wrapped.EditTappedThreadMaterial.SetSelectedItem(str(value) if value else '')

    @property
    def elastic_bending_resilience_of_clamped_parts(self) -> 'float':
        """float: 'ElasticBendingResilienceOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticBendingResilienceOfClampedParts

        if temp is None:
            return None

        return temp

    @property
    def elastic_bending_resilience_of_concentric_clamped_parts(self) -> 'float':
        """float: 'ElasticBendingResilienceOfConcentricClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticBendingResilienceOfConcentricClampedParts

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_clamped_parts_eccentric_clamping(self) -> 'float':
        """float: 'ElasticResilienceOfClampedPartsEccentricClamping' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfClampedPartsEccentricClamping

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_clamped_parts(self) -> 'float':
        """float: 'ElasticResilienceOfClampedParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfClampedParts

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_clamped_parts_eccentric_loading(self) -> 'float':
        """float: 'ElasticResilienceOfClampedPartsEccentricLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfClampedPartsEccentricLoading

        if temp is None:
            return None

        return temp

    @property
    def elastic_resilience_of_clamped_parts_in_operating_state(self) -> 'float':
        """float: 'ElasticResilienceOfClampedPartsInOperatingState' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticResilienceOfClampedPartsInOperatingState

        if temp is None:
            return None

        return temp

    @property
    def friction_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FrictionRadius' is the original name of this property."""

        temp = self.wrapped.FrictionRadius

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @friction_radius.setter
    def friction_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FrictionRadius = value

    @property
    def height(self) -> 'float':
        """float: 'Height' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Height

        if temp is None:
            return None

        return temp

    @property
    def inside_diameter_of_bearing_surface_of_washer(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'InsideDiameterOfBearingSurfaceOfWasher' is the original name of this property."""

        temp = self.wrapped.InsideDiameterOfBearingSurfaceOfWasher

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @inside_diameter_of_bearing_surface_of_washer.setter
    def inside_diameter_of_bearing_surface_of_washer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.InsideDiameterOfBearingSurfaceOfWasher = value

    @property
    def inside_diameter_of_head_bearing_area(self) -> 'float':
        """float: 'InsideDiameterOfHeadBearingArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InsideDiameterOfHeadBearingArea

        if temp is None:
            return None

        return temp

    @property
    def inside_diameter_of_plane_head_bearing_surface(self) -> 'float':
        """float: 'InsideDiameterOfPlaneHeadBearingSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InsideDiameterOfPlaneHeadBearingSurface

        if temp is None:
            return None

        return temp

    @property
    def is_concentrically_clamped(self) -> 'bool':
        """bool: 'IsConcentricallyClamped' is the original name of this property."""

        temp = self.wrapped.IsConcentricallyClamped

        if temp is None:
            return None

        return temp

    @is_concentrically_clamped.setter
    def is_concentrically_clamped(self, value: 'bool'):
        self.wrapped.IsConcentricallyClamped = bool(value) if value else False

    @property
    def joint_coefficient(self) -> 'float':
        """float: 'JointCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.JointCoefficient

        if temp is None:
            return None

        return temp

    @property
    def joint_geometry(self) -> '_1286.JointGeometries':
        """JointGeometries: 'JointGeometry' is the original name of this property."""

        temp = self.wrapped.JointGeometry

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1286.JointGeometries)(value) if value is not None else None

    @joint_geometry.setter
    def joint_geometry(self, value: '_1286.JointGeometries'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.JointGeometry = value

    @property
    def length_ratio(self) -> 'float':
        """float: 'LengthRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthRatio

        if temp is None:
            return None

        return temp

    @property
    def length_of_deformation_cone(self) -> 'float':
        """float: 'LengthOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfDeformationCone

        if temp is None:
            return None

        return temp

    @property
    def length_of_deformation_sleeve(self) -> 'float':
        """float: 'LengthOfDeformationSleeve' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfDeformationSleeve

        if temp is None:
            return None

        return temp

    @property
    def length_of_free_loaded_thread(self) -> 'float':
        """float: 'LengthOfFreeLoadedThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfFreeLoadedThread

        if temp is None:
            return None

        return temp

    @property
    def limiting_outside_diameter_maximum_diameter_of_deformation_cone(self) -> 'float':
        """float: 'LimitingOutsideDiameterMaximumDiameterOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingOutsideDiameterMaximumDiameterOfDeformationCone

        if temp is None:
            return None

        return temp

    @property
    def limiting_value_of_interface_dsv(self) -> 'float':
        """float: 'LimitingValueOfInterfaceDSV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingValueOfInterfaceDSV

        if temp is None:
            return None

        return temp

    @property
    def limiting_value_of_interface_esv(self) -> 'float':
        """float: 'LimitingValueOfInterfaceESV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingValueOfInterfaceESV

        if temp is None:
            return None

        return temp

    @property
    def limiting_value_of_interface_esv_with_recessed_tapped_hole(self) -> 'float':
        """float: 'LimitingValueOfInterfaceESVWithRecessedTappedHole' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitingValueOfInterfaceESVWithRecessedTappedHole

        if temp is None:
            return None

        return temp

    @property
    def maximum_coefficient_of_friction_of_bearing_area(self) -> 'float':
        """float: 'MaximumCoefficientOfFrictionOfBearingArea' is the original name of this property."""

        temp = self.wrapped.MaximumCoefficientOfFrictionOfBearingArea

        if temp is None:
            return None

        return temp

    @maximum_coefficient_of_friction_of_bearing_area.setter
    def maximum_coefficient_of_friction_of_bearing_area(self, value: 'float'):
        self.wrapped.MaximumCoefficientOfFrictionOfBearingArea = float(value) if value else 0.0

    @property
    def maximum_coefficient_of_friction_of_thread(self) -> 'float':
        """float: 'MaximumCoefficientOfFrictionOfThread' is the original name of this property."""

        temp = self.wrapped.MaximumCoefficientOfFrictionOfThread

        if temp is None:
            return None

        return temp

    @maximum_coefficient_of_friction_of_thread.setter
    def maximum_coefficient_of_friction_of_thread(self, value: 'float'):
        self.wrapped.MaximumCoefficientOfFrictionOfThread = float(value) if value else 0.0

    @property
    def maximum_outside_diameter_of_deformation_cone(self) -> 'float':
        """float: 'MaximumOutsideDiameterOfDeformationCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumOutsideDiameterOfDeformationCone

        if temp is None:
            return None

        return temp

    @property
    def measurement_interface_area_perpendicular_to_width(self) -> 'float':
        """float: 'MeasurementInterfaceAreaPerpendicularToWidth' is the original name of this property."""

        temp = self.wrapped.MeasurementInterfaceAreaPerpendicularToWidth

        if temp is None:
            return None

        return temp

    @measurement_interface_area_perpendicular_to_width.setter
    def measurement_interface_area_perpendicular_to_width(self, value: 'float'):
        self.wrapped.MeasurementInterfaceAreaPerpendicularToWidth = float(value) if value else 0.0

    @property
    def minimum_assembly_bearing_area_of_head(self) -> 'float':
        """float: 'MinimumAssemblyBearingAreaOfHead' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAssemblyBearingAreaOfHead

        if temp is None:
            return None

        return temp

    @property
    def minimum_assembly_bearing_area_of_nut(self) -> 'float':
        """float: 'MinimumAssemblyBearingAreaOfNut' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAssemblyBearingAreaOfNut

        if temp is None:
            return None

        return temp

    @property
    def minimum_bearing_area(self) -> 'float':
        """float: 'MinimumBearingArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumBearingArea

        if temp is None:
            return None

        return temp

    @property
    def minimum_coefficient_of_friction_at_interface(self) -> 'float':
        """float: 'MinimumCoefficientOfFrictionAtInterface' is the original name of this property."""

        temp = self.wrapped.MinimumCoefficientOfFrictionAtInterface

        if temp is None:
            return None

        return temp

    @minimum_coefficient_of_friction_at_interface.setter
    def minimum_coefficient_of_friction_at_interface(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionAtInterface = float(value) if value else 0.0

    @property
    def minimum_coefficient_of_friction_of_bearing_area(self) -> 'float':
        """float: 'MinimumCoefficientOfFrictionOfBearingArea' is the original name of this property."""

        temp = self.wrapped.MinimumCoefficientOfFrictionOfBearingArea

        if temp is None:
            return None

        return temp

    @minimum_coefficient_of_friction_of_bearing_area.setter
    def minimum_coefficient_of_friction_of_bearing_area(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionOfBearingArea = float(value) if value else 0.0

    @property
    def minimum_coefficient_of_friction_of_thread(self) -> 'float':
        """float: 'MinimumCoefficientOfFrictionOfThread' is the original name of this property."""

        temp = self.wrapped.MinimumCoefficientOfFrictionOfThread

        if temp is None:
            return None

        return temp

    @minimum_coefficient_of_friction_of_thread.setter
    def minimum_coefficient_of_friction_of_thread(self, value: 'float'):
        self.wrapped.MinimumCoefficientOfFrictionOfThread = float(value) if value else 0.0

    @property
    def minimum_plate_thickness(self) -> 'float':
        """float: 'MinimumPlateThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumPlateThickness

        if temp is None:
            return None

        return temp

    @property
    def moment_of_gyration_of_cross_section_at_minor_thread_diameter(self) -> 'float':
        """float: 'MomentOfGyrationOfCrossSectionAtMinorThreadDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MomentOfGyrationOfCrossSectionAtMinorThreadDiameter

        if temp is None:
            return None

        return temp

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

    @property
    def nominal_cross_section(self) -> 'float':
        """float: 'NominalCrossSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalCrossSection

        if temp is None:
            return None

        return temp

    @property
    def nominal_cross_section_of_hollow_bolt(self) -> 'float':
        """float: 'NominalCrossSectionOfHollowBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalCrossSectionOfHollowBolt

        if temp is None:
            return None

        return temp

    @property
    def number_of_bolt_sections(self) -> 'int':
        """int: 'NumberOfBoltSections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfBoltSections

        if temp is None:
            return None

        return temp

    @property
    def number_of_force_transmitting_interfaces(self) -> 'int':
        """int: 'NumberOfForceTransmittingInterfaces' is the original name of this property."""

        temp = self.wrapped.NumberOfForceTransmittingInterfaces

        if temp is None:
            return None

        return temp

    @number_of_force_transmitting_interfaces.setter
    def number_of_force_transmitting_interfaces(self, value: 'int'):
        self.wrapped.NumberOfForceTransmittingInterfaces = int(value) if value else 0

    @property
    def number_of_torque_transmitting_interfaces(self) -> 'int':
        """int: 'NumberOfTorqueTransmittingInterfaces' is the original name of this property."""

        temp = self.wrapped.NumberOfTorqueTransmittingInterfaces

        if temp is None:
            return None

        return temp

    @number_of_torque_transmitting_interfaces.setter
    def number_of_torque_transmitting_interfaces(self, value: 'int'):
        self.wrapped.NumberOfTorqueTransmittingInterfaces = int(value) if value else 0

    @property
    def nut_chamfer_diameter(self) -> 'float':
        """float: 'NutChamferDiameter' is the original name of this property."""

        temp = self.wrapped.NutChamferDiameter

        if temp is None:
            return None

        return temp

    @nut_chamfer_diameter.setter
    def nut_chamfer_diameter(self, value: 'float'):
        self.wrapped.NutChamferDiameter = float(value) if value else 0.0

    @property
    def outside_diameter_of_bearing_surface_of_washer(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'OutsideDiameterOfBearingSurfaceOfWasher' is the original name of this property."""

        temp = self.wrapped.OutsideDiameterOfBearingSurfaceOfWasher

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @outside_diameter_of_bearing_surface_of_washer.setter
    def outside_diameter_of_bearing_surface_of_washer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.OutsideDiameterOfBearingSurfaceOfWasher = value

    @property
    def outside_diameter_of_nut(self) -> 'float':
        """float: 'OutsideDiameterOfNut' is the original name of this property."""

        temp = self.wrapped.OutsideDiameterOfNut

        if temp is None:
            return None

        return temp

    @outside_diameter_of_nut.setter
    def outside_diameter_of_nut(self, value: 'float'):
        self.wrapped.OutsideDiameterOfNut = float(value) if value else 0.0

    @property
    def reduction_coefficient(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ReductionCoefficient' is the original name of this property."""

        temp = self.wrapped.ReductionCoefficient

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @reduction_coefficient.setter
    def reduction_coefficient(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ReductionCoefficient = value

    @property
    def rolled_before_or_after_heat_treatment(self) -> '_1289.RolledBeforeOrAfterHeatTreament':
        """RolledBeforeOrAfterHeatTreament: 'RolledBeforeOrAfterHeatTreatment' is the original name of this property."""

        temp = self.wrapped.RolledBeforeOrAfterHeatTreatment

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1289.RolledBeforeOrAfterHeatTreament)(value) if value is not None else None

    @rolled_before_or_after_heat_treatment.setter
    def rolled_before_or_after_heat_treatment(self, value: '_1289.RolledBeforeOrAfterHeatTreament'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RolledBeforeOrAfterHeatTreatment = value

    @property
    def sealing_area(self) -> 'float':
        """float: 'SealingArea' is the original name of this property."""

        temp = self.wrapped.SealingArea

        if temp is None:
            return None

        return temp

    @sealing_area.setter
    def sealing_area(self, value: 'float'):
        self.wrapped.SealingArea = float(value) if value else 0.0

    @property
    def section_radii_of_gyration(self) -> 'List[float]':
        """List[float]: 'SectionRadiiOfGyration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SectionRadiiOfGyration

        if temp is None:
            return None

        value = conversion.to_list_any(temp)
        return value

    @property
    def shearing_area_transverse_loading(self) -> 'float':
        """float: 'ShearingAreaTransverseLoading' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearingAreaTransverseLoading

        if temp is None:
            return None

        return temp

    @property
    def stress_cross_sectional_area(self) -> 'float':
        """float: 'StressCrossSectionalArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressCrossSectionalArea

        if temp is None:
            return None

        return temp

    @property
    def stress_diameter(self) -> 'float':
        """float: 'StressDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StressDiameter

        if temp is None:
            return None

        return temp

    @property
    def substitutional_bending_length_of_bolt(self) -> 'float':
        """float: 'SubstitutionalBendingLengthOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalBendingLengthOfBolt

        if temp is None:
            return None

        return temp

    @property
    def substitutional_extension_length_of_engaged_nut_thread(self) -> 'float':
        """float: 'SubstitutionalExtensionLengthOfEngagedNutThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalExtensionLengthOfEngagedNutThread

        if temp is None:
            return None

        return temp

    @property
    def substitutional_extension_length_of_engaged_thread(self) -> 'float':
        """float: 'SubstitutionalExtensionLengthOfEngagedThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalExtensionLengthOfEngagedThread

        if temp is None:
            return None

        return temp

    @property
    def substitutional_extension_length_of_head(self) -> 'float':
        """float: 'SubstitutionalExtensionLengthOfHead' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalExtensionLengthOfHead

        if temp is None:
            return None

        return temp

    @property
    def substitutional_moment_of_gyration_of_cone(self) -> 'float':
        """float: 'SubstitutionalMomentOfGyrationOfCone' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalMomentOfGyrationOfCone

        if temp is None:
            return None

        return temp

    @property
    def substitutional_moment_of_gyration_of_plates(self) -> 'float':
        """float: 'SubstitutionalMomentOfGyrationOfPlates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalMomentOfGyrationOfPlates

        if temp is None:
            return None

        return temp

    @property
    def substitutional_moment_of_gyration_of_plates_minus_bolt_area(self) -> 'float':
        """float: 'SubstitutionalMomentOfGyrationOfPlatesMinusBoltArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalMomentOfGyrationOfPlatesMinusBoltArea

        if temp is None:
            return None

        return temp

    @property
    def substitutional_moment_of_gyration_of_sleeve(self) -> 'float':
        """float: 'SubstitutionalMomentOfGyrationOfSleeve' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SubstitutionalMomentOfGyrationOfSleeve

        if temp is None:
            return None

        return temp

    @property
    def substitutional_outside_diameter_of_basic_solid(self) -> 'float':
        """float: 'SubstitutionalOutsideDiameterOfBasicSolid' is the original name of this property."""

        temp = self.wrapped.SubstitutionalOutsideDiameterOfBasicSolid

        if temp is None:
            return None

        return temp

    @substitutional_outside_diameter_of_basic_solid.setter
    def substitutional_outside_diameter_of_basic_solid(self, value: 'float'):
        self.wrapped.SubstitutionalOutsideDiameterOfBasicSolid = float(value) if value else 0.0

    @property
    def substitutional_outside_diameter_of_basic_solid_at_interface(self) -> 'float':
        """float: 'SubstitutionalOutsideDiameterOfBasicSolidAtInterface' is the original name of this property."""

        temp = self.wrapped.SubstitutionalOutsideDiameterOfBasicSolidAtInterface

        if temp is None:
            return None

        return temp

    @substitutional_outside_diameter_of_basic_solid_at_interface.setter
    def substitutional_outside_diameter_of_basic_solid_at_interface(self, value: 'float'):
        self.wrapped.SubstitutionalOutsideDiameterOfBasicSolidAtInterface = float(value) if value else 0.0

    @property
    def total_axial_resilience(self) -> 'float':
        """float: 'TotalAxialResilience' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalAxialResilience

        if temp is None:
            return None

        return temp

    @property
    def total_bending_resilience(self) -> 'float':
        """float: 'TotalBendingResilience' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalBendingResilience

        if temp is None:
            return None

        return temp

    @property
    def utilization_factor(self) -> 'float':
        """float: 'UtilizationFactor' is the original name of this property."""

        temp = self.wrapped.UtilizationFactor

        if temp is None:
            return None

        return temp

    @utilization_factor.setter
    def utilization_factor(self, value: 'float'):
        self.wrapped.UtilizationFactor = float(value) if value else 0.0

    @property
    def washer_thickness(self) -> 'float':
        """float: 'WasherThickness' is the original name of this property."""

        temp = self.wrapped.WasherThickness

        if temp is None:
            return None

        return temp

    @washer_thickness.setter
    def washer_thickness(self, value: 'float'):
        self.wrapped.WasherThickness = float(value) if value else 0.0

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return None

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def bolt_geometry(self) -> '_1274.BoltGeometry':
        """BoltGeometry: 'BoltGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_bolt(self) -> '_1276.BoltMaterial':
        """BoltMaterial: 'MaterialOfBolt' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialOfBolt

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_nut(self) -> '_1272.BoltedJointMaterial':
        """BoltedJointMaterial: 'MaterialOfNut' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialOfNut

        if temp is None:
            return None

        if _1272.BoltedJointMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material_of_nut to BoltedJointMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def material_of_tapped_thread(self) -> '_1272.BoltedJointMaterial':
        """BoltedJointMaterial: 'MaterialOfTappedThread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialOfTappedThread

        if temp is None:
            return None

        if _1272.BoltedJointMaterial.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast material_of_tapped_thread to BoltedJointMaterial. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def orientation(self) -> 'Vector3D':
        """Vector3D: 'Orientation' is the original name of this property."""

        temp = self.wrapped.Orientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @orientation.setter
    def orientation(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Orientation = value

    @property
    def clamped_sections(self) -> 'List[_1281.ClampedSection]':
        """List[ClampedSection]: 'ClampedSections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ClampedSections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
