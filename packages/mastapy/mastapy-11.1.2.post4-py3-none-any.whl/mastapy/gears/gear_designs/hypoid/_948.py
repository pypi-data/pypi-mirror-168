"""_948.py

HypoidGearDesign
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.agma_gleason_conical import _1147
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Hypoid', 'HypoidGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearDesign',)


class HypoidGearDesign(_1147.AGMAGleasonConicalGearDesign):
    """HypoidGearDesign

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'HypoidGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Addendum

        if temp is None:
            return None

        return temp

    @property
    def addendum_angle(self) -> 'float':
        """float: 'AddendumAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumAngle

        if temp is None:
            return None

        return temp

    @property
    def crown_to_crossing_point(self) -> 'float':
        """float: 'CrownToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrownToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Dedendum

        if temp is None:
            return None

        return temp

    @property
    def dedendum_angle(self) -> 'float':
        """float: 'DedendumAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DedendumAngle

        if temp is None:
            return None

        return temp

    @property
    def face_angle(self) -> 'float':
        """float: 'FaceAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceAngle

        if temp is None:
            return None

        return temp

    @property
    def face_apex_to_crossing_point(self) -> 'float':
        """float: 'FaceApexToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceApexToCrossingPoint

        if temp is None:
            return None

        return temp

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
    def front_crown_to_crossing_point(self) -> 'float':
        """float: 'FrontCrownToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrontCrownToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def geometry_factor_j(self) -> 'float':
        """float: 'GeometryFactorJ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJ

        if temp is None:
            return None

        return temp

    @property
    def inner_cone_distance(self) -> 'float':
        """float: 'InnerConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerConeDistance

        if temp is None:
            return None

        return temp

    @property
    def mean_addendum(self) -> 'float':
        """float: 'MeanAddendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanAddendum

        if temp is None:
            return None

        return temp

    @property
    def mean_cone_distance(self) -> 'float':
        """float: 'MeanConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanConeDistance

        if temp is None:
            return None

        return temp

    @property
    def mean_dedendum(self) -> 'float':
        """float: 'MeanDedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanDedendum

        if temp is None:
            return None

        return temp

    @property
    def mean_normal_circular_thickness(self) -> 'float':
        """float: 'MeanNormalCircularThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalCircularThickness

        if temp is None:
            return None

        return temp

    @property
    def mean_normal_topland(self) -> 'float':
        """float: 'MeanNormalTopland' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalTopland

        if temp is None:
            return None

        return temp

    @property
    def mean_pitch_diameter(self) -> 'float':
        """float: 'MeanPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanPitchDiameter

        if temp is None:
            return None

        return temp

    @property
    def mean_point_to_crossing_point(self) -> 'float':
        """float: 'MeanPointToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanPointToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def mean_radius(self) -> 'float':
        """float: 'MeanRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanRadius

        if temp is None:
            return None

        return temp

    @property
    def mean_root_spiral_angle(self) -> 'float':
        """float: 'MeanRootSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanRootSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def mean_spiral_angle(self) -> 'float':
        """float: 'MeanSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanSpiralAngle

        if temp is None:
            return None

        return temp

    @property
    def offset_angle_in_axial_plane(self) -> 'float':
        """float: 'OffsetAngleInAxialPlane' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OffsetAngleInAxialPlane

        if temp is None:
            return None

        return temp

    @property
    def outer_cone_distance(self) -> 'float':
        """float: 'OuterConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterConeDistance

        if temp is None:
            return None

        return temp

    @property
    def outer_tip_diameter(self) -> 'float':
        """float: 'OuterTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterTipDiameter

        if temp is None:
            return None

        return temp

    @property
    def outer_whole_depth(self) -> 'float':
        """float: 'OuterWholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterWholeDepth

        if temp is None:
            return None

        return temp

    @property
    def outer_working_depth(self) -> 'float':
        """float: 'OuterWorkingDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterWorkingDepth

        if temp is None:
            return None

        return temp

    @property
    def pitch_angle(self) -> 'float':
        """float: 'PitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchAngle

        if temp is None:
            return None

        return temp

    @property
    def pitch_apex_to_crossing_point(self) -> 'float':
        """float: 'PitchApexToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def pitch_apex_to_crown(self) -> 'float':
        """float: 'PitchApexToCrown' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToCrown

        if temp is None:
            return None

        return temp

    @property
    def pitch_diameter(self) -> 'float':
        """float: 'PitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchDiameter

        if temp is None:
            return None

        return temp

    @property
    def root_apex_to_crossing_point(self) -> 'float':
        """float: 'RootApexToCrossingPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootApexToCrossingPoint

        if temp is None:
            return None

        return temp

    @property
    def strength_factor_q(self) -> 'float':
        """float: 'StrengthFactorQ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StrengthFactorQ

        if temp is None:
            return None

        return temp
