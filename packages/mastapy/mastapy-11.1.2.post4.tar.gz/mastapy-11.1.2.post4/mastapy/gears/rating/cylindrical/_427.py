"""_427.py

CylindricalGearMeshRating
"""


from typing import List

from mastapy.gears import _295, _313
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility_gui.charts import (
    _1634, _1625, _1630, _1631
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical.agma import _502
from mastapy.gears.gear_designs.cylindrical import _982
from mastapy.gears.rating.cylindrical import _437, _434, _429
from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _457, _459, _461
from mastapy.gears.rating.cylindrical.iso6336 import (
    _479, _481, _483, _485,
    _487
)
from mastapy.gears.rating.cylindrical.din3990 import _500
from mastapy.gears.load_case.cylindrical import _850
from mastapy.gears.rating.cylindrical.vdi import _456
from mastapy.gears.rating import _332
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshRating',)


class CylindricalGearMeshRating(_332.GearMeshRating):
    """CylindricalGearMeshRating

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_295.CylindricalFlanks':
        """CylindricalFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_295.CylindricalFlanks)(value) if value is not None else None

    @property
    def load_intensity(self) -> 'float':
        """float: 'LoadIntensity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadIntensity

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_factor(self) -> 'float':
        """float: 'LoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactor

        if temp is None:
            return None

        return temp

    @property
    def load_sharing_factor_source(self) -> '_313.PlanetaryRatingLoadSharingOption':
        """PlanetaryRatingLoadSharingOption: 'LoadSharingFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingFactorSource

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_313.PlanetaryRatingLoadSharingOption)(value) if value is not None else None

    @property
    def mechanical_advantage(self) -> 'float':
        """float: 'MechanicalAdvantage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MechanicalAdvantage

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction(self) -> 'float':
        """float: 'MeshCoefficientOfFriction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFriction

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_benedict_and_kelley(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionBenedictAndKelley

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_drozdov_and_gavrikov(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionDrozdovAndGavrikov' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionDrozdovAndGavrikov

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_isotc60(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionISOTC60' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionISOTC60

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_isotr1417912001(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionISOTR1417912001' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionISOTR1417912001

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_isotr1417912001_with_surface_roughness_parameter(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionISOTR1417912001WithSurfaceRoughnessParameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionISOTR1417912001WithSurfaceRoughnessParameter

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_isotr1417922001_martins_et_al(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionISOTR1417922001MartinsEtAl' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionISOTR1417922001MartinsEtAl

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_isotr1417922001(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionISOTR1417922001' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionISOTR1417922001

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_misharin(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionMisharin' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionMisharin

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_o_donoghue_and_cameron(self) -> 'float':
        """float: 'MeshCoefficientOfFrictionODonoghueAndCameron' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionODonoghueAndCameron

        if temp is None:
            return None

        return temp

    @property
    def mesh_coefficient_of_friction_at_diameter_benedict_and_kelley(self) -> '_1634.TwoDChartDefinition':
        """TwoDChartDefinition: 'MeshCoefficientOfFrictionAtDiameterBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshCoefficientOfFrictionAtDiameterBenedictAndKelley

        if temp is None:
            return None

        if _1634.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_coefficient_of_friction_at_diameter_benedict_and_kelley to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def sliding_ratio_at_end_of_recess(self) -> 'float':
        """float: 'SlidingRatioAtEndOfRecess' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingRatioAtEndOfRecess

        if temp is None:
            return None

        return temp

    @property
    def sliding_ratio_at_start_of_approach(self) -> 'float':
        """float: 'SlidingRatioAtStartOfApproach' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingRatioAtStartOfApproach

        if temp is None:
            return None

        return temp

    @property
    def tooth_loss_factor(self) -> 'float':
        """float: 'ToothLossFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothLossFactor

        if temp is None:
            return None

        return temp

    @property
    def agma_cylindrical_mesh_single_flank_rating(self) -> '_502.AGMA2101MeshSingleFlankRating':
        """AGMA2101MeshSingleFlankRating: 'AGMACylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AGMACylindricalMeshSingleFlankRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_mesh(self) -> '_982.CylindricalGearMeshDesign':
        """CylindricalGearMeshDesign: 'CylindricalGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating(self) -> '_437.CylindricalMeshSingleFlankRating':
        """CylindricalMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _437.CylindricalMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to CylindricalMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(self) -> '_457.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating':
        """MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _457.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_plastic_gear_vdi2736_abstract_mesh_single_flank_rating(self) -> '_459.PlasticGearVDI2736AbstractMeshSingleFlankRating':
        """PlasticGearVDI2736AbstractMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _459.PlasticGearVDI2736AbstractMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to PlasticGearVDI2736AbstractMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_plastic_plastic_vdi2736_mesh_single_flank_rating(self) -> '_461.PlasticPlasticVDI2736MeshSingleFlankRating':
        """PlasticPlasticVDI2736MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _461.PlasticPlasticVDI2736MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to PlasticPlasticVDI2736MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_479.ISO63361996MeshSingleFlankRating':
        """ISO63361996MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _479.ISO63361996MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_481.ISO63362006MeshSingleFlankRating':
        """ISO63362006MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _481.ISO63362006MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_483.ISO63362019MeshSingleFlankRating':
        """ISO63362019MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _483.ISO63362019MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso6336_abstract_mesh_single_flank_rating(self) -> '_485.ISO6336AbstractMeshSingleFlankRating':
        """ISO6336AbstractMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _485.ISO6336AbstractMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO6336AbstractMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_iso6336_abstract_metal_mesh_single_flank_rating(self) -> '_487.ISO6336AbstractMetalMeshSingleFlankRating':
        """ISO6336AbstractMetalMeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _487.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_500.DIN3990MeshSingleFlankRating':
        """DIN3990MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _500.DIN3990MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_mesh_single_flank_rating_of_type_agma2101_mesh_single_flank_rating(self) -> '_502.AGMA2101MeshSingleFlankRating':
        """AGMA2101MeshSingleFlankRating: 'CylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _502.AGMA2101MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast cylindrical_mesh_single_flank_rating to AGMA2101MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_rating(self) -> '_434.CylindricalGearSetRating':
        """CylindricalGearSetRating: 'GearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating(self) -> '_487.ISO6336AbstractMetalMeshSingleFlankRating':
        """ISO6336AbstractMetalMeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _487.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_479.ISO63361996MeshSingleFlankRating':
        """ISO63361996MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _479.ISO63361996MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_481.ISO63362006MeshSingleFlankRating':
        """ISO63362006MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _481.ISO63362006MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_483.ISO63362019MeshSingleFlankRating':
        """ISO63362019MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _483.ISO63362019MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def isodin_cylindrical_mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_500.DIN3990MeshSingleFlankRating':
        """DIN3990MeshSingleFlankRating: 'ISODINCylindricalMeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ISODINCylindricalMeshSingleFlankRating

        if temp is None:
            return None

        if _500.DIN3990MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast isodin_cylindrical_mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_load_case(self) -> '_850.CylindricalMeshLoadCase':
        """CylindricalMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating(self) -> '_437.CylindricalMeshSingleFlankRating':
        """CylindricalMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _437.CylindricalMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to CylindricalMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_metal_plastic_or_plastic_metal_vdi2736_mesh_single_flank_rating(self) -> '_457.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating':
        """MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _457.MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to MetalPlasticOrPlasticMetalVDI2736MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_plastic_gear_vdi2736_abstract_mesh_single_flank_rating(self) -> '_459.PlasticGearVDI2736AbstractMeshSingleFlankRating':
        """PlasticGearVDI2736AbstractMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _459.PlasticGearVDI2736AbstractMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to PlasticGearVDI2736AbstractMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_plastic_plastic_vdi2736_mesh_single_flank_rating(self) -> '_461.PlasticPlasticVDI2736MeshSingleFlankRating':
        """PlasticPlasticVDI2736MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _461.PlasticPlasticVDI2736MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to PlasticPlasticVDI2736MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_iso63361996_mesh_single_flank_rating(self) -> '_479.ISO63361996MeshSingleFlankRating':
        """ISO63361996MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _479.ISO63361996MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63361996MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_iso63362006_mesh_single_flank_rating(self) -> '_481.ISO63362006MeshSingleFlankRating':
        """ISO63362006MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _481.ISO63362006MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_iso63362019_mesh_single_flank_rating(self) -> '_483.ISO63362019MeshSingleFlankRating':
        """ISO63362019MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _483.ISO63362019MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362019MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_iso6336_abstract_mesh_single_flank_rating(self) -> '_485.ISO6336AbstractMeshSingleFlankRating':
        """ISO6336AbstractMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _485.ISO6336AbstractMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO6336AbstractMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_iso6336_abstract_metal_mesh_single_flank_rating(self) -> '_487.ISO6336AbstractMetalMeshSingleFlankRating':
        """ISO6336AbstractMetalMeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _487.ISO6336AbstractMetalMeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO6336AbstractMetalMeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_din3990_mesh_single_flank_rating(self) -> '_500.DIN3990MeshSingleFlankRating':
        """DIN3990MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _500.DIN3990MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to DIN3990MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating_of_type_agma2101_mesh_single_flank_rating(self) -> '_502.AGMA2101MeshSingleFlankRating':
        """AGMA2101MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _502.AGMA2101MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to AGMA2101MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def vdi_cylindrical_gear_single_flank_rating(self) -> '_456.VDI2737InternalGearSingleFlankRating':
        """VDI2737InternalGearSingleFlankRating: 'VDICylindricalGearSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VDICylindricalGearSingleFlankRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_ratings(self) -> 'List[_429.CylindricalGearRating]':
        """List[CylindricalGearRating]: 'CylindricalGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
