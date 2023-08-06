"""_1166.py

PointsWithWorstResults
"""


from mastapy.gears.ltca.cylindrical import _825
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_POINTS_WITH_WORST_RESULTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'PointsWithWorstResults')


__docformat__ = 'restructuredtext en'
__all__ = ('PointsWithWorstResults',)


class PointsWithWorstResults(_0.APIBase):
    """PointsWithWorstResults

    This is a mastapy class.
    """

    TYPE = _POINTS_WITH_WORST_RESULTS

    def __init__(self, instance_to_wrap: 'PointsWithWorstResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFrictionBenedictAndKelley

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def depth_of_max_shear_stress(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'DepthOfMaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaxShearStress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force_per_unit_length(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ForcePerUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForcePerUnitLength

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gap_between_loaded_flanks_transverse(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GapBetweenLoadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapBetweenLoadedFlanksTransverse

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gap_between_unloaded_flanks_transverse(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapBetweenUnloadedFlanksTransverse

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GearADepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearADepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_a_maximum_material_exposure_iso633642019(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GearAMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GearBDepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBDepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_b_maximum_material_exposure_iso633642019(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'GearBMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hertzian_contact_half_width(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactHalfWidth

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def max_pressure(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxPressure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def max_shear_stress(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxShearStress

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_contact_temperature_isotr1514412010(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412010

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412014

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_contact_temperature_isots6336222018(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTS6336222018

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_flash_temperature_isotr1514412010(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412010

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412014

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_flash_temperature_isots6336222018(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTS6336222018

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_safety_factor_isotr1514412010(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412010

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412014

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting_safety_factor_isots6336222018(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTS6336222018

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def minimum_lubricant_film_thickness_isotr1514412010(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def minimum_lubricant_film_thickness_isotr1514412014(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def minimum_lubricant_film_thickness_isots6336222018(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def pressure_velocity_pv(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureVelocityPV

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_contact_temperature_agma925a03(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureAGMA925A03

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_contact_temperature_din399041987(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureDIN399041987

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTR1398912000

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_contact_temperature_isots6336202017(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTS6336202017

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_flash_temperature_agma925a03(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureAGMA925A03

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_flash_temperature_din399041987(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureDIN399041987

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTR1398912000

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_flash_temperature_isots6336202017(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTS6336202017

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_safety_factor_agma925a03(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorAGMA925A03

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_safety_factor_din399041987(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorDIN399041987

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTR1398912000

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing_safety_factor_isots6336202017(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTS6336202017

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sliding_power_loss(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingPowerLoss

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sliding_velocity(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specific_lubricant_film_thickness_isotr1514412010(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specific_lubricant_film_thickness_isotr1514412014(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def specific_lubricant_film_thickness_isots6336222018(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def total_deflection_for_mesh(self) -> '_825.CylindricalGearMeshLoadedContactPoint':
        """CylindricalGearMeshLoadedContactPoint: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalDeflectionForMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
