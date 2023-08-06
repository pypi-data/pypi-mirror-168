"""_1758.py

LoadedBallBearingElement
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling import _1730, _1772
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_ELEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingElement')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingElement',)


class LoadedBallBearingElement(_1772.LoadedElement):
    """LoadedBallBearingElement

    This is a mastapy class.
    """

    TYPE = _LOADED_BALL_BEARING_ELEMENT

    def __init__(self, instance_to_wrap: 'LoadedBallBearingElement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_velocity(self) -> 'float':
        """float: 'AngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularVelocity

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_left_raceway_inside_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerLeftRacewayInsideEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerLeftRacewayInsideEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_raceway_inner_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerRacewayInnerEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerRacewayInnerEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_raceway_left_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerRacewayLeftEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerRacewayLeftEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_raceway_outer_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerRacewayOuterEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerRacewayOuterEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_raceway_right_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerRacewayRightEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerRacewayRightEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_inner_right_raceway_inside_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfInnerRightRacewayInsideEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfInnerRightRacewayInsideEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_left_raceway_inside_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterLeftRacewayInsideEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterLeftRacewayInsideEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_raceway_inner_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterRacewayInnerEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterRacewayInnerEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_raceway_left_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterRacewayLeftEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterRacewayLeftEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_raceway_outer_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterRacewayOuterEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterRacewayOuterEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_raceway_right_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterRacewayRightEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterRacewayRightEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def arc_distance_of_outer_right_raceway_inside_edge_to_hertzian_contact(self) -> 'float':
        """float: 'ArcDistanceOfOuterRightRacewayInsideEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ArcDistanceOfOuterRightRacewayInsideEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def centrifugal_force(self) -> 'float':
        """float: 'CentrifugalForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentrifugalForce

        if temp is None:
            return None

        return temp

    @property
    def contact_angle_inner(self) -> 'float':
        """float: 'ContactAngleInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleInner

        if temp is None:
            return None

        return temp

    @property
    def contact_angle_outer(self) -> 'float':
        """float: 'ContactAngleOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactAngleOuter

        if temp is None:
            return None

        return temp

    @property
    def depth_of_maximum_shear_stress_inner(self) -> 'float':
        """float: 'DepthOfMaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaximumShearStressInner

        if temp is None:
            return None

        return temp

    @property
    def depth_of_maximum_shear_stress_outer(self) -> 'float':
        """float: 'DepthOfMaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaximumShearStressOuter

        if temp is None:
            return None

        return temp

    @property
    def difference_between_cage_speed_and_orbit_speed(self) -> 'float':
        """float: 'DifferenceBetweenCageSpeedAndOrbitSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DifferenceBetweenCageSpeedAndOrbitSpeed

        if temp is None:
            return None

        return temp

    @property
    def gyroscopic_moment(self) -> 'float':
        """float: 'GyroscopicMoment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GyroscopicMoment

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_left_race_inside_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerLeftRaceInsideEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerLeftRaceInsideEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_left(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_race_inner_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerRaceInnerEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRaceInnerEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_race_outer_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerRaceOuterEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRaceOuterEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_right_race_inside_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerRightRaceInsideEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRightRaceInsideEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_inner_right(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationInnerRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationInnerRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_left_race_inside_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterLeftRaceInsideEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterLeftRaceInsideEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_left(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterLeft

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_race_inner_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterRaceInnerEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRaceInnerEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_race_outer_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterRaceOuterEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRaceOuterEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_right_race_inside_edge(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterRightRaceInsideEdge' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRightRaceInsideEdge

        if temp is None:
            return None

        return temp

    @property
    def hertzian_ellipse_major_2b_track_truncation_outer_right(self) -> 'float':
        """float: 'HertzianEllipseMajor2bTrackTruncationOuterRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianEllipseMajor2bTrackTruncationOuterRight

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_inner(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionInner

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_major_dimension_outer(self) -> 'float':
        """float: 'HertzianSemiMajorDimensionOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMajorDimensionOuter

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_inner(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionInner

        if temp is None:
            return None

        return temp

    @property
    def hertzian_semi_minor_dimension_outer(self) -> 'float':
        """float: 'HertzianSemiMinorDimensionOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianSemiMinorDimensionOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_inner(self) -> 'float':
        """float: 'MaximumNormalStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_normal_stress_outer(self) -> 'float':
        """float: 'MaximumNormalStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumNormalStressOuter

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_inner(self) -> 'float':
        """float: 'MaximumShearStressInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressInner

        if temp is None:
            return None

        return temp

    @property
    def maximum_shear_stress_outer(self) -> 'float':
        """float: 'MaximumShearStressOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumShearStressOuter

        if temp is None:
            return None

        return temp

    @property
    def number_of_contact_points(self) -> 'int':
        """int: 'NumberOfContactPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfContactPoints

        if temp is None:
            return None

        return temp

    @property
    def orbit_speed_ignoring_cage(self) -> 'float':
        """float: 'OrbitSpeedIgnoringCage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OrbitSpeedIgnoringCage

        if temp is None:
            return None

        return temp

    @property
    def smallest_arc_distance_of_raceway_edge_to_hertzian_contact(self) -> 'float':
        """float: 'SmallestArcDistanceOfRacewayEdgeToHertzianContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SmallestArcDistanceOfRacewayEdgeToHertzianContact

        if temp is None:
            return None

        return temp

    @property
    def spinto_roll_ratio_inner(self) -> 'float':
        """float: 'SpintoRollRatioInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpintoRollRatioInner

        if temp is None:
            return None

        return temp

    @property
    def spinto_roll_ratio_outer(self) -> 'float':
        """float: 'SpintoRollRatioOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpintoRollRatioOuter

        if temp is None:
            return None

        return temp

    @property
    def surface_velocity(self) -> 'float':
        """float: 'SurfaceVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceVelocity

        if temp is None:
            return None

        return temp

    @property
    def track_truncation_occurring_beyond_permissible_limit(self) -> 'bool':
        """bool: 'TrackTruncationOccurringBeyondPermissibleLimit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TrackTruncationOccurringBeyondPermissibleLimit

        if temp is None:
            return None

        return temp

    @property
    def worst_hertzian_ellipse_major_2b_track_truncation(self) -> 'float':
        """float: 'WorstHertzianEllipseMajor2bTrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorstHertzianEllipseMajor2bTrackTruncation

        if temp is None:
            return None

        return temp

    @property
    def inner_race_contact_geometries(self) -> 'List[_1730.BallBearingRaceContactGeometry]':
        """List[BallBearingRaceContactGeometry]: 'InnerRaceContactGeometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerRaceContactGeometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def outer_race_contact_geometries(self) -> 'List[_1730.BallBearingRaceContactGeometry]':
        """List[BallBearingRaceContactGeometry]: 'OuterRaceContactGeometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterRaceContactGeometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
