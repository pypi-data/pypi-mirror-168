"""_1712.py

LoadedBearingResults
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1723
from mastapy.bearings.bearing_designs import (
    _1888, _1889, _1890, _1891,
    _1892
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1893, _1894, _1895, _1896,
    _1897, _1898, _1900, _1905,
    _1906, _1907, _1910, _1915,
    _1916, _1917, _1918, _1921,
    _1922, _1925, _1926, _1927,
    _1928, _1929, _1930
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1943, _1945, _1947, _1949,
    _1950, _1951
)
from mastapy.bearings.bearing_designs.concept import _1953, _1954, _1955
from mastapy.math_utility.measured_vectors import _1371
from mastapy.bearings.bearing_results.rolling import _1827
from mastapy.bearings import _1642
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingResults',)


class LoadedBearingResults(_1642.BearingLoadCaseResultsLightweight):
    """LoadedBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_of_gravity_from_z_axis(self) -> 'float':
        """float: 'AngleOfGravityFromZAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleOfGravityFromZAxis

        if temp is None:
            return None

        return temp

    @property
    def axial_displacement_preload(self) -> 'float':
        """float: 'AxialDisplacementPreload' is the original name of this property."""

        temp = self.wrapped.AxialDisplacementPreload

        if temp is None:
            return None

        return temp

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'float'):
        self.wrapped.AxialDisplacementPreload = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        """float: 'Duration' is the original name of this property."""

        temp = self.wrapped.Duration

        if temp is None:
            return None

        return temp

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def force_results_are_overridden(self) -> 'bool':
        """bool: 'ForceResultsAreOverridden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceResultsAreOverridden

        if temp is None:
            return None

        return temp

    @property
    def inner_ring_angular_velocity(self) -> 'float':
        """float: 'InnerRingAngularVelocity' is the original name of this property."""

        temp = self.wrapped.InnerRingAngularVelocity

        if temp is None:
            return None

        return temp

    @inner_ring_angular_velocity.setter
    def inner_ring_angular_velocity(self, value: 'float'):
        self.wrapped.InnerRingAngularVelocity = float(value) if value else 0.0

    @property
    def orientation(self) -> '_1723.Orientations':
        """Orientations: 'Orientation' is the original name of this property."""

        temp = self.wrapped.Orientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1723.Orientations)(value) if value is not None else None

    @orientation.setter
    def orientation(self, value: '_1723.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def outer_ring_angular_velocity(self) -> 'float':
        """float: 'OuterRingAngularVelocity' is the original name of this property."""

        temp = self.wrapped.OuterRingAngularVelocity

        if temp is None:
            return None

        return temp

    @outer_ring_angular_velocity.setter
    def outer_ring_angular_velocity(self, value: 'float'):
        self.wrapped.OuterRingAngularVelocity = float(value) if value else 0.0

    @property
    def relative_angular_velocity(self) -> 'float':
        """float: 'RelativeAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeAngularVelocity

        if temp is None:
            return None

        return temp

    @property
    def relative_axial_displacement(self) -> 'float':
        """float: 'RelativeAxialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeAxialDisplacement

        if temp is None:
            return None

        return temp

    @property
    def relative_radial_displacement(self) -> 'float':
        """float: 'RelativeRadialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeRadialDisplacement

        if temp is None:
            return None

        return temp

    @property
    def signed_relative_angular_velocity(self) -> 'float':
        """float: 'SignedRelativeAngularVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SignedRelativeAngularVelocity

        if temp is None:
            return None

        return temp

    @property
    def specified_axial_internal_clearance(self) -> 'float':
        """float: 'SpecifiedAxialInternalClearance' is the original name of this property."""

        temp = self.wrapped.SpecifiedAxialInternalClearance

        if temp is None:
            return None

        return temp

    @specified_axial_internal_clearance.setter
    def specified_axial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedAxialInternalClearance = float(value) if value else 0.0

    @property
    def specified_radial_internal_clearance(self) -> 'float':
        """float: 'SpecifiedRadialInternalClearance' is the original name of this property."""

        temp = self.wrapped.SpecifiedRadialInternalClearance

        if temp is None:
            return None

        return temp

    @specified_radial_internal_clearance.setter
    def specified_radial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedRadialInternalClearance = float(value) if value else 0.0

    @property
    def bearing(self) -> '_1888.BearingDesign':
        """BearingDesign: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1888.BearingDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to BearingDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_detailed_bearing(self) -> '_1889.DetailedBearing':
        """DetailedBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1889.DetailedBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to DetailedBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_dummy_rolling_bearing(self) -> '_1890.DummyRollingBearing':
        """DummyRollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1890.DummyRollingBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to DummyRollingBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_linear_bearing(self) -> '_1891.LinearBearing':
        """LinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1891.LinearBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to LinearBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_non_linear_bearing(self) -> '_1892.NonLinearBearing':
        """NonLinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1892.NonLinearBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonLinearBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_angular_contact_ball_bearing(self) -> '_1893.AngularContactBallBearing':
        """AngularContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1893.AngularContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_angular_contact_thrust_ball_bearing(self) -> '_1894.AngularContactThrustBallBearing':
        """AngularContactThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1894.AngularContactThrustBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactThrustBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_asymmetric_spherical_roller_bearing(self) -> '_1895.AsymmetricSphericalRollerBearing':
        """AsymmetricSphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1895.AsymmetricSphericalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to AsymmetricSphericalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1896.AxialThrustCylindricalRollerBearing':
        """AxialThrustCylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1896.AxialThrustCylindricalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_axial_thrust_needle_roller_bearing(self) -> '_1897.AxialThrustNeedleRollerBearing':
        """AxialThrustNeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1897.AxialThrustNeedleRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustNeedleRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_ball_bearing(self) -> '_1898.BallBearing':
        """BallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1898.BallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to BallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_barrel_roller_bearing(self) -> '_1900.BarrelRollerBearing':
        """BarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1900.BarrelRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to BarrelRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_crossed_roller_bearing(self) -> '_1905.CrossedRollerBearing':
        """CrossedRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1905.CrossedRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to CrossedRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_cylindrical_roller_bearing(self) -> '_1906.CylindricalRollerBearing':
        """CylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1906.CylindricalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to CylindricalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_deep_groove_ball_bearing(self) -> '_1907.DeepGrooveBallBearing':
        """DeepGrooveBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1907.DeepGrooveBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to DeepGrooveBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_four_point_contact_ball_bearing(self) -> '_1910.FourPointContactBallBearing':
        """FourPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1910.FourPointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to FourPointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_multi_point_contact_ball_bearing(self) -> '_1915.MultiPointContactBallBearing':
        """MultiPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1915.MultiPointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to MultiPointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_needle_roller_bearing(self) -> '_1916.NeedleRollerBearing':
        """NeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1916.NeedleRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to NeedleRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_non_barrel_roller_bearing(self) -> '_1917.NonBarrelRollerBearing':
        """NonBarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1917.NonBarrelRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonBarrelRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_roller_bearing(self) -> '_1918.RollerBearing':
        """RollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1918.RollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_rolling_bearing(self) -> '_1921.RollingBearing':
        """RollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1921.RollingBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollingBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_self_aligning_ball_bearing(self) -> '_1922.SelfAligningBallBearing':
        """SelfAligningBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1922.SelfAligningBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to SelfAligningBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_spherical_roller_bearing(self) -> '_1925.SphericalRollerBearing':
        """SphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1925.SphericalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_spherical_roller_thrust_bearing(self) -> '_1926.SphericalRollerThrustBearing':
        """SphericalRollerThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1926.SphericalRollerThrustBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerThrustBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_taper_roller_bearing(self) -> '_1927.TaperRollerBearing':
        """TaperRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1927.TaperRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to TaperRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_three_point_contact_ball_bearing(self) -> '_1928.ThreePointContactBallBearing':
        """ThreePointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1928.ThreePointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThreePointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_thrust_ball_bearing(self) -> '_1929.ThrustBallBearing':
        """ThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1929.ThrustBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThrustBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_toroidal_roller_bearing(self) -> '_1930.ToroidalRollerBearing':
        """ToroidalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1930.ToroidalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ToroidalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_pad_fluid_film_bearing(self) -> '_1943.PadFluidFilmBearing':
        """PadFluidFilmBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1943.PadFluidFilmBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to PadFluidFilmBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_plain_grease_filled_journal_bearing(self) -> '_1945.PlainGreaseFilledJournalBearing':
        """PlainGreaseFilledJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1945.PlainGreaseFilledJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainGreaseFilledJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_plain_journal_bearing(self) -> '_1947.PlainJournalBearing':
        """PlainJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1947.PlainJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_plain_oil_fed_journal_bearing(self) -> '_1949.PlainOilFedJournalBearing':
        """PlainOilFedJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1949.PlainOilFedJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainOilFedJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_tilting_pad_journal_bearing(self) -> '_1950.TiltingPadJournalBearing':
        """TiltingPadJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1950.TiltingPadJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_tilting_pad_thrust_bearing(self) -> '_1951.TiltingPadThrustBearing':
        """TiltingPadThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1951.TiltingPadThrustBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadThrustBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_concept_axial_clearance_bearing(self) -> '_1953.ConceptAxialClearanceBearing':
        """ConceptAxialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1953.ConceptAxialClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptAxialClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_concept_clearance_bearing(self) -> '_1954.ConceptClearanceBearing':
        """ConceptClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1954.ConceptClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_of_type_concept_radial_clearance_bearing(self) -> '_1955.ConceptRadialClearanceBearing':
        """ConceptRadialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearing

        if temp is None:
            return None

        if _1955.ConceptRadialClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptRadialClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_on_inner_race(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'ForceOnInnerRace' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceOnInnerRace

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ring_results(self) -> 'List[_1827.RingForceAndDisplacement]':
        """List[RingForceAndDisplacement]: 'RingResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
