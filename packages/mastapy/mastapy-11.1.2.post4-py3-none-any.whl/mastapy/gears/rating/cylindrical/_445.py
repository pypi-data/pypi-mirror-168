"""_445.py

MicroPittingResultsRow
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MICRO_PITTING_RESULTS_ROW = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'MicroPittingResultsRow')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroPittingResultsRow',)


class MicroPittingResultsRow(_0.APIBase):
    """MicroPittingResultsRow

    This is a mastapy class.
    """

    TYPE = _MICRO_PITTING_RESULTS_ROW

    def __init__(self, instance_to_wrap: 'MicroPittingResultsRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_point(self) -> 'float':
        """float: 'ContactPoint' is the original name of this property."""

        temp = self.wrapped.ContactPoint

        if temp is None:
            return None

        return temp

    @contact_point.setter
    def contact_point(self, value: 'float'):
        self.wrapped.ContactPoint = float(value) if value else 0.0

    @property
    def dynamic_viscosity_of_the_lubricant_at_contact_temperature(self) -> 'float':
        """float: 'DynamicViscosityOfTheLubricantAtContactTemperature' is the original name of this property."""

        temp = self.wrapped.DynamicViscosityOfTheLubricantAtContactTemperature

        if temp is None:
            return None

        return temp

    @dynamic_viscosity_of_the_lubricant_at_contact_temperature.setter
    def dynamic_viscosity_of_the_lubricant_at_contact_temperature(self, value: 'float'):
        self.wrapped.DynamicViscosityOfTheLubricantAtContactTemperature = float(value) if value else 0.0

    @property
    def kinematic_viscosity_of_lubricant_at_contact_temperature(self) -> 'float':
        """float: 'KinematicViscosityOfLubricantAtContactTemperature' is the original name of this property."""

        temp = self.wrapped.KinematicViscosityOfLubricantAtContactTemperature

        if temp is None:
            return None

        return temp

    @kinematic_viscosity_of_lubricant_at_contact_temperature.setter
    def kinematic_viscosity_of_lubricant_at_contact_temperature(self, value: 'float'):
        self.wrapped.KinematicViscosityOfLubricantAtContactTemperature = float(value) if value else 0.0

    @property
    def load_sharing_factor(self) -> 'float':
        """float: 'LoadSharingFactor' is the original name of this property."""

        temp = self.wrapped.LoadSharingFactor

        if temp is None:
            return None

        return temp

    @load_sharing_factor.setter
    def load_sharing_factor(self, value: 'float'):
        self.wrapped.LoadSharingFactor = float(value) if value else 0.0

    @property
    def local_contact_temperature(self) -> 'float':
        """float: 'LocalContactTemperature' is the original name of this property."""

        temp = self.wrapped.LocalContactTemperature

        if temp is None:
            return None

        return temp

    @local_contact_temperature.setter
    def local_contact_temperature(self, value: 'float'):
        self.wrapped.LocalContactTemperature = float(value) if value else 0.0

    @property
    def local_flash_temperature(self) -> 'float':
        """float: 'LocalFlashTemperature' is the original name of this property."""

        temp = self.wrapped.LocalFlashTemperature

        if temp is None:
            return None

        return temp

    @local_flash_temperature.setter
    def local_flash_temperature(self, value: 'float'):
        self.wrapped.LocalFlashTemperature = float(value) if value else 0.0

    @property
    def local_hertzian_contact_stress(self) -> 'float':
        """float: 'LocalHertzianContactStress' is the original name of this property."""

        temp = self.wrapped.LocalHertzianContactStress

        if temp is None:
            return None

        return temp

    @local_hertzian_contact_stress.setter
    def local_hertzian_contact_stress(self, value: 'float'):
        self.wrapped.LocalHertzianContactStress = float(value) if value else 0.0

    @property
    def local_load_parameter(self) -> 'float':
        """float: 'LocalLoadParameter' is the original name of this property."""

        temp = self.wrapped.LocalLoadParameter

        if temp is None:
            return None

        return temp

    @local_load_parameter.setter
    def local_load_parameter(self, value: 'float'):
        self.wrapped.LocalLoadParameter = float(value) if value else 0.0

    @property
    def local_lubricant_film_thickness(self) -> 'float':
        """float: 'LocalLubricantFilmThickness' is the original name of this property."""

        temp = self.wrapped.LocalLubricantFilmThickness

        if temp is None:
            return None

        return temp

    @local_lubricant_film_thickness.setter
    def local_lubricant_film_thickness(self, value: 'float'):
        self.wrapped.LocalLubricantFilmThickness = float(value) if value else 0.0

    @property
    def local_sliding_parameter(self) -> 'float':
        """float: 'LocalSlidingParameter' is the original name of this property."""

        temp = self.wrapped.LocalSlidingParameter

        if temp is None:
            return None

        return temp

    @local_sliding_parameter.setter
    def local_sliding_parameter(self, value: 'float'):
        self.wrapped.LocalSlidingParameter = float(value) if value else 0.0

    @property
    def local_sliding_velocity(self) -> 'float':
        """float: 'LocalSlidingVelocity' is the original name of this property."""

        temp = self.wrapped.LocalSlidingVelocity

        if temp is None:
            return None

        return temp

    @local_sliding_velocity.setter
    def local_sliding_velocity(self, value: 'float'):
        self.wrapped.LocalSlidingVelocity = float(value) if value else 0.0

    @property
    def local_velocity_parameter(self) -> 'float':
        """float: 'LocalVelocityParameter' is the original name of this property."""

        temp = self.wrapped.LocalVelocityParameter

        if temp is None:
            return None

        return temp

    @local_velocity_parameter.setter
    def local_velocity_parameter(self, value: 'float'):
        self.wrapped.LocalVelocityParameter = float(value) if value else 0.0

    @property
    def lubricant_density_at_contact_temperature(self) -> 'float':
        """float: 'LubricantDensityAtContactTemperature' is the original name of this property."""

        temp = self.wrapped.LubricantDensityAtContactTemperature

        if temp is None:
            return None

        return temp

    @lubricant_density_at_contact_temperature.setter
    def lubricant_density_at_contact_temperature(self, value: 'float'):
        self.wrapped.LubricantDensityAtContactTemperature = float(value) if value else 0.0

    @property
    def mesh(self) -> 'str':
        """str: 'Mesh' is the original name of this property."""

        temp = self.wrapped.Mesh

        if temp is None:
            return None

        return temp

    @mesh.setter
    def mesh(self, value: 'str'):
        self.wrapped.Mesh = str(value) if value else ''

    @property
    def mesh_diameter_of_pinion(self) -> 'float':
        """float: 'MeshDiameterOfPinion' is the original name of this property."""

        temp = self.wrapped.MeshDiameterOfPinion

        if temp is None:
            return None

        return temp

    @mesh_diameter_of_pinion.setter
    def mesh_diameter_of_pinion(self, value: 'float'):
        self.wrapped.MeshDiameterOfPinion = float(value) if value else 0.0

    @property
    def mesh_diameter_of_wheel(self) -> 'float':
        """float: 'MeshDiameterOfWheel' is the original name of this property."""

        temp = self.wrapped.MeshDiameterOfWheel

        if temp is None:
            return None

        return temp

    @mesh_diameter_of_wheel.setter
    def mesh_diameter_of_wheel(self, value: 'float'):
        self.wrapped.MeshDiameterOfWheel = float(value) if value else 0.0

    @property
    def normal_relative_radius_of_curvature(self) -> 'float':
        """float: 'NormalRelativeRadiusOfCurvature' is the original name of this property."""

        temp = self.wrapped.NormalRelativeRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @normal_relative_radius_of_curvature.setter
    def normal_relative_radius_of_curvature(self, value: 'float'):
        self.wrapped.NormalRelativeRadiusOfCurvature = float(value) if value else 0.0

    @property
    def pinion_diameter(self) -> 'float':
        """float: 'PinionDiameter' is the original name of this property."""

        temp = self.wrapped.PinionDiameter

        if temp is None:
            return None

        return temp

    @pinion_diameter.setter
    def pinion_diameter(self, value: 'float'):
        self.wrapped.PinionDiameter = float(value) if value else 0.0

    @property
    def pinion_flank_radius_of_curvature(self) -> 'float':
        """float: 'PinionFlankRadiusOfCurvature' is the original name of this property."""

        temp = self.wrapped.PinionFlankRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @pinion_flank_radius_of_curvature.setter
    def pinion_flank_radius_of_curvature(self, value: 'float'):
        self.wrapped.PinionFlankRadiusOfCurvature = float(value) if value else 0.0

    @property
    def pinion_radius(self) -> 'float':
        """float: 'PinionRadius' is the original name of this property."""

        temp = self.wrapped.PinionRadius

        if temp is None:
            return None

        return temp

    @pinion_radius.setter
    def pinion_radius(self, value: 'float'):
        self.wrapped.PinionRadius = float(value) if value else 0.0

    @property
    def pinion_roll_angle(self) -> 'float':
        """float: 'PinionRollAngle' is the original name of this property."""

        temp = self.wrapped.PinionRollAngle

        if temp is None:
            return None

        return temp

    @pinion_roll_angle.setter
    def pinion_roll_angle(self, value: 'float'):
        self.wrapped.PinionRollAngle = float(value) if value else 0.0

    @property
    def pinion_roll_distance(self) -> 'float':
        """float: 'PinionRollDistance' is the original name of this property."""

        temp = self.wrapped.PinionRollDistance

        if temp is None:
            return None

        return temp

    @pinion_roll_distance.setter
    def pinion_roll_distance(self, value: 'float'):
        self.wrapped.PinionRollDistance = float(value) if value else 0.0

    @property
    def point_of_mesh(self) -> 'str':
        """str: 'PointOfMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointOfMesh

        if temp is None:
            return None

        return temp

    @property
    def pressure_viscosity_coefficient_at_contact_temperature(self) -> 'float':
        """float: 'PressureViscosityCoefficientAtContactTemperature' is the original name of this property."""

        temp = self.wrapped.PressureViscosityCoefficientAtContactTemperature

        if temp is None:
            return None

        return temp

    @pressure_viscosity_coefficient_at_contact_temperature.setter
    def pressure_viscosity_coefficient_at_contact_temperature(self, value: 'float'):
        self.wrapped.PressureViscosityCoefficientAtContactTemperature = float(value) if value else 0.0

    @property
    def sum_of_tangential_velocities(self) -> 'float':
        """float: 'SumOfTangentialVelocities' is the original name of this property."""

        temp = self.wrapped.SumOfTangentialVelocities

        if temp is None:
            return None

        return temp

    @sum_of_tangential_velocities.setter
    def sum_of_tangential_velocities(self, value: 'float'):
        self.wrapped.SumOfTangentialVelocities = float(value) if value else 0.0

    @property
    def transverse_relative_radius_of_curvature(self) -> 'float':
        """float: 'TransverseRelativeRadiusOfCurvature' is the original name of this property."""

        temp = self.wrapped.TransverseRelativeRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @transverse_relative_radius_of_curvature.setter
    def transverse_relative_radius_of_curvature(self, value: 'float'):
        self.wrapped.TransverseRelativeRadiusOfCurvature = float(value) if value else 0.0

    @property
    def wheel_flank_radius_of_curvature(self) -> 'float':
        """float: 'WheelFlankRadiusOfCurvature' is the original name of this property."""

        temp = self.wrapped.WheelFlankRadiusOfCurvature

        if temp is None:
            return None

        return temp

    @wheel_flank_radius_of_curvature.setter
    def wheel_flank_radius_of_curvature(self, value: 'float'):
        self.wrapped.WheelFlankRadiusOfCurvature = float(value) if value else 0.0
