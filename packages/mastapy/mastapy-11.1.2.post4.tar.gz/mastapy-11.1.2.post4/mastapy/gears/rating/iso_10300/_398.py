"""_398.py

ISO10300MeshSingleFlankRatingMethodB2
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import (
    _366, _352, _355, _363
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.iso_10300 import _394
from mastapy._internal.python_net import python_net_import

_ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B2 = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'ISO10300MeshSingleFlankRatingMethodB2')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO10300MeshSingleFlankRatingMethodB2',)


class ISO10300MeshSingleFlankRatingMethodB2(_394.ISO10300MeshSingleFlankRating['_363.VirtualCylindricalGearISO10300MethodB2']):
    """ISO10300MeshSingleFlankRatingMethodB2

    This is a mastapy class.
    """

    TYPE = _ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B2

    def __init__(self, instance_to_wrap: 'ISO10300MeshSingleFlankRatingMethodB2.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_stress_method_b2(self) -> 'float':
        """float: 'ContactStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressMethodB2

        if temp is None:
            return None

        return temp

    @property
    def contact_stress_adjustment_factor(self) -> 'float':
        """float: 'ContactStressAdjustmentFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressAdjustmentFactor

        if temp is None:
            return None

        return temp

    @property
    def face_width_factor(self) -> 'float':
        """float: 'FaceWidthFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidthFactor

        if temp is None:
            return None

        return temp

    @property
    def inertia_factor_value_x(self) -> 'float':
        """float: 'InertiaFactorValueX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InertiaFactorValueX

        if temp is None:
            return None

        return temp

    @property
    def intermediate_value_x(self) -> 'float':
        """float: 'IntermediateValueX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IntermediateValueX

        if temp is None:
            return None

        return temp

    @property
    def length_of_action_at_critical_point(self) -> 'float':
        """float: 'LengthOfActionAtCriticalPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionAtCriticalPoint

        if temp is None:
            return None

        return temp

    @property
    def length_of_action_considering_adjacent_teeth(self) -> 'float':
        """float: 'LengthOfActionConsideringAdjacentTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionConsideringAdjacentTeeth

        if temp is None:
            return None

        return temp

    @property
    def length_of_contact_line(self) -> 'float':
        """float: 'LengthOfContactLine' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfContactLine

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_ratio_for_bending_method_b2(self) -> 'float':
        """float: 'LoadSharingRatioForBendingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingRatioForBendingMethodB2

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_ratio_for_pitting_method_b2(self) -> 'float':
        """float: 'LoadSharingRatioForPittingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingRatioForPittingMethodB2

        if temp is None:
            return None

        return temp

    @property
    def nominal_value_of_contact_stress_method_b2(self) -> 'float':
        """float: 'NominalValueOfContactStressMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalValueOfContactStressMethodB2

        if temp is None:
            return None

        return temp

    @property
    def pinion_profile_radius_of_curvature(self) -> 'float':
        """float: 'PinionProfileRadiusOfCurvature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionProfileRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @property
    def pitting_resistance_geometry_factor(self) -> 'float':
        """float: 'PittingResistanceGeometryFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PittingResistanceGeometryFactor

        if temp is None:
            return None

        return temp

    @property
    def position_change_alone_path_of_contact(self) -> 'float':
        """float: 'PositionChangeAlonePathOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PositionChangeAlonePathOfContact

        if temp is None:
            return None

        return temp

    @property
    def radius_of_curvature_change(self) -> 'float':
        """float: 'RadiusOfCurvatureChange' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadiusOfCurvatureChange

        if temp is None:
            return None

        return temp

    @property
    def relative_length_of_action_ellipse_contact(self) -> 'float':
        """float: 'RelativeLengthOfActionEllipseContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeLengthOfActionEllipseContact

        if temp is None:
            return None

        return temp

    @property
    def relative_length_of_action_ellipse_contact_for_statically_loaded_straight_bevel_and_zerol_bevel_gears(self) -> 'float':
        """float: 'RelativeLengthOfActionEllipseContactForStaticallyLoadedStraightBevelAndZerolBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeLengthOfActionEllipseContactForStaticallyLoadedStraightBevelAndZerolBevelGears

        if temp is None:
            return None

        return temp

    @property
    def relative_length_of_action_within_the_contact_ellipse(self) -> 'float':
        """float: 'RelativeLengthOfActionWithinTheContactEllipse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeLengthOfActionWithinTheContactEllipse

        if temp is None:
            return None

        return temp

    @property
    def relative_radius_of_profile_curvature_between_pinion_and_wheel(self) -> 'float':
        """float: 'RelativeRadiusOfProfileCurvatureBetweenPinionAndWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeRadiusOfProfileCurvatureBetweenPinionAndWheel

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factors_for_bending_method_b2(self) -> 'float':
        """float: 'TransverseLoadFactorsForBendingMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorsForBendingMethodB2

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factors_for_contact_method_b2(self) -> 'float':
        """float: 'TransverseLoadFactorsForContactMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorsForContactMethodB2

        if temp is None:
            return None

        return temp

    @property
    def wheel_profile_radius_of_curvature(self) -> 'float':
        """float: 'WheelProfileRadiusOfCurvature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelProfileRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @property
    def yi(self) -> 'float':
        """float: 'YI' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YI

        if temp is None:
            return None

        return temp

    @property
    def yi_for_bevel_and_zerol_bevel_gear(self) -> 'float':
        """float: 'YIForBevelAndZerolBevelGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YIForBevelAndZerolBevelGear

        if temp is None:
            return None

        return temp

    @property
    def yi_for_hypoid_gear(self) -> 'float':
        """float: 'YIForHypoidGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.YIForHypoidGear

        if temp is None:
            return None

        return temp

    @property
    def virtual_cylindrical_gear_set_method_b2(self) -> '_366.VirtualCylindricalGearSetISO10300MethodB2':
        """VirtualCylindricalGearSetISO10300MethodB2: 'VirtualCylindricalGearSetMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB2

        if temp is None:
            return None

        if _366.VirtualCylindricalGearSetISO10300MethodB2.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b2 to VirtualCylindricalGearSetISO10300MethodB2. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_cylindrical_gear_set_method_b2_of_type_bevel_virtual_cylindrical_gear_set_iso10300_method_b2(self) -> '_352.BevelVirtualCylindricalGearSetISO10300MethodB2':
        """BevelVirtualCylindricalGearSetISO10300MethodB2: 'VirtualCylindricalGearSetMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB2

        if temp is None:
            return None

        if _352.BevelVirtualCylindricalGearSetISO10300MethodB2.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b2 to BevelVirtualCylindricalGearSetISO10300MethodB2. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def virtual_cylindrical_gear_set_method_b2_of_type_hypoid_virtual_cylindrical_gear_set_iso10300_method_b2(self) -> '_355.HypoidVirtualCylindricalGearSetISO10300MethodB2':
        """HypoidVirtualCylindricalGearSetISO10300MethodB2: 'VirtualCylindricalGearSetMethodB2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualCylindricalGearSetMethodB2

        if temp is None:
            return None

        if _355.HypoidVirtualCylindricalGearSetISO10300MethodB2.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast virtual_cylindrical_gear_set_method_b2 to HypoidVirtualCylindricalGearSetISO10300MethodB2. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
