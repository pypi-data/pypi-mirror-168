"""_1880.py

LoadedPlainJournalBearingResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.fluid_film import _1881, _1877
from mastapy._internal.python_net import python_net_import

_LOADED_PLAIN_JOURNAL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.FluidFilm', 'LoadedPlainJournalBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedPlainJournalBearingResults',)


class LoadedPlainJournalBearingResults(_1877.LoadedFluidFilmBearingResults):
    """LoadedPlainJournalBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_PLAIN_JOURNAL_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedPlainJournalBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_position_of_the_minimum_film_thickness_from_the_x_axis(self) -> 'float':
        """float: 'AngularPositionOfTheMinimumFilmThicknessFromTheXAxis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularPositionOfTheMinimumFilmThicknessFromTheXAxis

        if temp is None:
            return None

        return temp

    @property
    def attitude_angle(self) -> 'float':
        """float: 'AttitudeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttitudeAngle

        if temp is None:
            return None

        return temp

    @property
    def attitude_force(self) -> 'float':
        """float: 'AttitudeForce' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AttitudeForce

        if temp is None:
            return None

        return temp

    @property
    def eccentricity_ratio(self) -> 'float':
        """float: 'EccentricityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EccentricityRatio

        if temp is None:
            return None

        return temp

    @property
    def kinematic_viscosity(self) -> 'float':
        """float: 'KinematicViscosity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KinematicViscosity

        if temp is None:
            return None

        return temp

    @property
    def lubricant_density(self) -> 'float':
        """float: 'LubricantDensity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricantDensity

        if temp is None:
            return None

        return temp

    @property
    def minimum_central_film_thickness(self) -> 'float':
        """float: 'MinimumCentralFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumCentralFilmThickness

        if temp is None:
            return None

        return temp

    @property
    def non_dimensional_load(self) -> 'float':
        """float: 'NonDimensionalLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NonDimensionalLoad

        if temp is None:
            return None

        return temp

    @property
    def non_dimensional_power_loss(self) -> 'float':
        """float: 'NonDimensionalPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NonDimensionalPowerLoss

        if temp is None:
            return None

        return temp

    @property
    def operating_temperature(self) -> 'float':
        """float: 'OperatingTemperature' is the original name of this property."""

        temp = self.wrapped.OperatingTemperature

        if temp is None:
            return None

        return temp

    @operating_temperature.setter
    def operating_temperature(self, value: 'float'):
        self.wrapped.OperatingTemperature = float(value) if value else 0.0

    @property
    def pressure_velocity(self) -> 'float':
        """float: 'PressureVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureVelocity

        if temp is None:
            return None

        return temp

    @property
    def radial_load_per_unit_of_projected_area(self) -> 'float':
        """float: 'RadialLoadPerUnitOfProjectedArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialLoadPerUnitOfProjectedArea

        if temp is None:
            return None

        return temp

    @property
    def shaft_relative_rotation_speed(self) -> 'float':
        """float: 'ShaftRelativeRotationSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftRelativeRotationSpeed

        if temp is None:
            return None

        return temp

    @property
    def journal_bearing_rows(self) -> 'List[_1881.LoadedPlainJournalBearingRow]':
        """List[LoadedPlainJournalBearingRow]: 'JournalBearingRows' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.JournalBearingRows

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
