"""_1163.py

CylindricalGearLTCAContactCharts
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.gears.cylindrical import _1165
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LTCA_CONTACT_CHARTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'CylindricalGearLTCAContactCharts')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLTCAContactCharts',)


class CylindricalGearLTCAContactCharts(_1165.GearLTCAContactCharts):
    """CylindricalGearLTCAContactCharts

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_LTCA_CONTACT_CHARTS

    def __init__(self, instance_to_wrap: 'CylindricalGearLTCAContactCharts.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> 'Image':
        """Image: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoefficientOfFrictionBenedictAndKelley

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gap_between_unloaded_flanks_transverse(self) -> 'Image':
        """Image: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapBetweenUnloadedFlanksTransverse

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self) -> 'Image':
        """Image: 'GearADepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearADepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gear_a_maximum_material_exposure_iso633642019(self) -> 'Image':
        """Image: 'GearAMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearAMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self) -> 'Image':
        """Image: 'GearBDepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBDepthOfMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gear_b_maximum_material_exposure_iso633642019(self) -> 'Image':
        """Image: 'GearBMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearBMaximumMaterialExposureISO633642019

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_contact_temperature_isotr1514412010(self) -> 'Image':
        """Image: 'MicropittingContactTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412010

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> 'Image':
        """Image: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTR1514412014

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_contact_temperature_isots6336222018(self) -> 'Image':
        """Image: 'MicropittingContactTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingContactTemperatureISOTS6336222018

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_flash_temperature_isotr1514412010(self) -> 'Image':
        """Image: 'MicropittingFlashTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412010

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> 'Image':
        """Image: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTR1514412014

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_flash_temperature_isots6336222018(self) -> 'Image':
        """Image: 'MicropittingFlashTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingFlashTemperatureISOTS6336222018

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_safety_factor_isotr1514412010(self) -> 'Image':
        """Image: 'MicropittingSafetyFactorISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412010

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> 'Image':
        """Image: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTR1514412014

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def micropitting_safety_factor_isots6336222018(self) -> 'Image':
        """Image: 'MicropittingSafetyFactorISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicropittingSafetyFactorISOTS6336222018

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def minimum_lubricant_film_thickness_isotr1514412010(self) -> 'Image':
        """Image: 'MinimumLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def minimum_lubricant_film_thickness_isotr1514412014(self) -> 'Image':
        """Image: 'MinimumLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def minimum_lubricant_film_thickness_isots6336222018(self) -> 'Image':
        """Image: 'MinimumLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def pressure_velocity_pv(self) -> 'Image':
        """Image: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureVelocityPV

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_contact_temperature_agma925a03(self) -> 'Image':
        """Image: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureAGMA925A03

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_contact_temperature_din399041987(self) -> 'Image':
        """Image: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureDIN399041987

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> 'Image':
        """Image: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTR1398912000

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_contact_temperature_isots6336202017(self) -> 'Image':
        """Image: 'ScuffingContactTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingContactTemperatureISOTS6336202017

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_flash_temperature_agma925a03(self) -> 'Image':
        """Image: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureAGMA925A03

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_flash_temperature_din399041987(self) -> 'Image':
        """Image: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureDIN399041987

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> 'Image':
        """Image: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTR1398912000

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_flash_temperature_isots6336202017(self) -> 'Image':
        """Image: 'ScuffingFlashTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingFlashTemperatureISOTS6336202017

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_safety_factor_agma925a03(self) -> 'Image':
        """Image: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorAGMA925A03

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_safety_factor_din399041987(self) -> 'Image':
        """Image: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorDIN399041987

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> 'Image':
        """Image: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTR1398912000

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def scuffing_safety_factor_isots6336202017(self) -> 'Image':
        """Image: 'ScuffingSafetyFactorISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingSafetyFactorISOTS6336202017

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def sliding_power_loss(self) -> 'Image':
        """Image: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingPowerLoss

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def sliding_velocity(self) -> 'Image':
        """Image: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocity

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def specific_lubricant_film_thickness_isotr1514412010(self) -> 'Image':
        """Image: 'SpecificLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412010

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def specific_lubricant_film_thickness_isotr1514412014(self) -> 'Image':
        """Image: 'SpecificLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTR1514412014

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def specific_lubricant_film_thickness_isots6336222018(self) -> 'Image':
        """Image: 'SpecificLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecificLubricantFilmThicknessISOTS6336222018

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value
