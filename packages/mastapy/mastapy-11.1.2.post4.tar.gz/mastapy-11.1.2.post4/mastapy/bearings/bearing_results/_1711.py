"""_1711.py

LoadedBearingDutyCycle
"""


from typing import List

from mastapy._internal import constructor, conversion
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
from mastapy.utility.property import _1614
from mastapy.bearings import _1642
from mastapy.bearings.bearing_results import _1712
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingDutyCycle',)


class LoadedBearingDutyCycle(_0.APIBase):
    """LoadedBearingDutyCycle

    This is a mastapy class.
    """

    TYPE = _LOADED_BEARING_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'LoadedBearingDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duration(self) -> 'float':
        """float: 'Duration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Duration

        if temp is None:
            return None

        return temp

    @property
    def duty_cycle_name(self) -> 'str':
        """str: 'DutyCycleName' is the original name of this property."""

        temp = self.wrapped.DutyCycleName

        if temp is None:
            return None

        return temp

    @duty_cycle_name.setter
    def duty_cycle_name(self, value: 'str'):
        self.wrapped.DutyCycleName = str(value) if value else ''

    @property
    def bearing_design(self) -> '_1888.BearingDesign':
        """BearingDesign: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1888.BearingDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BearingDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_detailed_bearing(self) -> '_1889.DetailedBearing':
        """DetailedBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1889.DetailedBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DetailedBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_dummy_rolling_bearing(self) -> '_1890.DummyRollingBearing':
        """DummyRollingBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1890.DummyRollingBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DummyRollingBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_linear_bearing(self) -> '_1891.LinearBearing':
        """LinearBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1891.LinearBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to LinearBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_non_linear_bearing(self) -> '_1892.NonLinearBearing':
        """NonLinearBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1892.NonLinearBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NonLinearBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_angular_contact_ball_bearing(self) -> '_1893.AngularContactBallBearing':
        """AngularContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1893.AngularContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AngularContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_angular_contact_thrust_ball_bearing(self) -> '_1894.AngularContactThrustBallBearing':
        """AngularContactThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1894.AngularContactThrustBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AngularContactThrustBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_asymmetric_spherical_roller_bearing(self) -> '_1895.AsymmetricSphericalRollerBearing':
        """AsymmetricSphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1895.AsymmetricSphericalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AsymmetricSphericalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1896.AxialThrustCylindricalRollerBearing':
        """AxialThrustCylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1896.AxialThrustCylindricalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_axial_thrust_needle_roller_bearing(self) -> '_1897.AxialThrustNeedleRollerBearing':
        """AxialThrustNeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1897.AxialThrustNeedleRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to AxialThrustNeedleRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_ball_bearing(self) -> '_1898.BallBearing':
        """BallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1898.BallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_barrel_roller_bearing(self) -> '_1900.BarrelRollerBearing':
        """BarrelRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1900.BarrelRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to BarrelRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_crossed_roller_bearing(self) -> '_1905.CrossedRollerBearing':
        """CrossedRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1905.CrossedRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to CrossedRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_cylindrical_roller_bearing(self) -> '_1906.CylindricalRollerBearing':
        """CylindricalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1906.CylindricalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to CylindricalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_deep_groove_ball_bearing(self) -> '_1907.DeepGrooveBallBearing':
        """DeepGrooveBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1907.DeepGrooveBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to DeepGrooveBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_four_point_contact_ball_bearing(self) -> '_1910.FourPointContactBallBearing':
        """FourPointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1910.FourPointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to FourPointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_multi_point_contact_ball_bearing(self) -> '_1915.MultiPointContactBallBearing':
        """MultiPointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1915.MultiPointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to MultiPointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_needle_roller_bearing(self) -> '_1916.NeedleRollerBearing':
        """NeedleRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1916.NeedleRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NeedleRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_non_barrel_roller_bearing(self) -> '_1917.NonBarrelRollerBearing':
        """NonBarrelRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1917.NonBarrelRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to NonBarrelRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_roller_bearing(self) -> '_1918.RollerBearing':
        """RollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1918.RollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to RollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_rolling_bearing(self) -> '_1921.RollingBearing':
        """RollingBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1921.RollingBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to RollingBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_self_aligning_ball_bearing(self) -> '_1922.SelfAligningBallBearing':
        """SelfAligningBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1922.SelfAligningBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SelfAligningBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_spherical_roller_bearing(self) -> '_1925.SphericalRollerBearing':
        """SphericalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1925.SphericalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SphericalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_spherical_roller_thrust_bearing(self) -> '_1926.SphericalRollerThrustBearing':
        """SphericalRollerThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1926.SphericalRollerThrustBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to SphericalRollerThrustBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_taper_roller_bearing(self) -> '_1927.TaperRollerBearing':
        """TaperRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1927.TaperRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TaperRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_three_point_contact_ball_bearing(self) -> '_1928.ThreePointContactBallBearing':
        """ThreePointContactBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1928.ThreePointContactBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ThreePointContactBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_thrust_ball_bearing(self) -> '_1929.ThrustBallBearing':
        """ThrustBallBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1929.ThrustBallBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ThrustBallBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_toroidal_roller_bearing(self) -> '_1930.ToroidalRollerBearing':
        """ToroidalRollerBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1930.ToroidalRollerBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ToroidalRollerBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_pad_fluid_film_bearing(self) -> '_1943.PadFluidFilmBearing':
        """PadFluidFilmBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1943.PadFluidFilmBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PadFluidFilmBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_plain_grease_filled_journal_bearing(self) -> '_1945.PlainGreaseFilledJournalBearing':
        """PlainGreaseFilledJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1945.PlainGreaseFilledJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainGreaseFilledJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_plain_journal_bearing(self) -> '_1947.PlainJournalBearing':
        """PlainJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1947.PlainJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_plain_oil_fed_journal_bearing(self) -> '_1949.PlainOilFedJournalBearing':
        """PlainOilFedJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1949.PlainOilFedJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to PlainOilFedJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_tilting_pad_journal_bearing(self) -> '_1950.TiltingPadJournalBearing':
        """TiltingPadJournalBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1950.TiltingPadJournalBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TiltingPadJournalBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_tilting_pad_thrust_bearing(self) -> '_1951.TiltingPadThrustBearing':
        """TiltingPadThrustBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1951.TiltingPadThrustBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to TiltingPadThrustBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_concept_axial_clearance_bearing(self) -> '_1953.ConceptAxialClearanceBearing':
        """ConceptAxialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1953.ConceptAxialClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptAxialClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_concept_clearance_bearing(self) -> '_1954.ConceptClearanceBearing':
        """ConceptClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1954.ConceptClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def bearing_design_of_type_concept_radial_clearance_bearing(self) -> '_1955.ConceptRadialClearanceBearing':
        """ConceptRadialClearanceBearing: 'BearingDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingDesign

        if temp is None:
            return None

        if _1955.ConceptRadialClearanceBearing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast bearing_design to ConceptRadialClearanceBearing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def radial_load_summary(self) -> '_1614.DutyCyclePropertySummaryForce[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'RadialLoadSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialLoadSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def z_thrust_reaction_summary(self) -> '_1614.DutyCyclePropertySummaryForce[_1642.BearingLoadCaseResultsLightweight]':
        """DutyCyclePropertySummaryForce[BearingLoadCaseResultsLightweight]: 'ZThrustReactionSummary' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZThrustReactionSummary

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1642.BearingLoadCaseResultsLightweight](temp) if temp is not None else None

    @property
    def bearing_load_case_results(self) -> 'List[_1712.LoadedBearingResults]':
        """List[LoadedBearingResults]: 'BearingLoadCaseResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingLoadCaseResults

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
