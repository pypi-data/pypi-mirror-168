"""_2281.py

GearSet
"""


from typing import List

from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.gears.gear_designs import _913
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.zerol_bevel import _917
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _922
from mastapy.gears.gear_designs.straight_bevel import _926
from mastapy.gears.gear_designs.straight_bevel_diff import _930
from mastapy.gears.gear_designs.spiral_bevel import _934
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _938
from mastapy.gears.gear_designs.klingelnberg_hypoid import _942
from mastapy.gears.gear_designs.klingelnberg_conical import _946
from mastapy.gears.gear_designs.hypoid import _950
from mastapy.gears.gear_designs.face import _958
from mastapy.gears.gear_designs.cylindrical import _990, _1001
from mastapy.gears.gear_designs.conical import _1110
from mastapy.gears.gear_designs.concept import _1132
from mastapy.gears.gear_designs.bevel import _1136
from mastapy.gears.gear_designs.agma_gleason_conical import _1149
from mastapy.system_model.part_model import _2226
from mastapy._internal.python_net import python_net_import

_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSet',)


class GearSet(_2226.SpecialisedAssembly):
    """GearSet

    This is a mastapy class.
    """

    TYPE = _GEAR_SET

    def __init__(self, instance_to_wrap: 'GearSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_design(self) -> 'list_with_selected_item.ListWithSelectedItem_GearSetDesign':
        """list_with_selected_item.ListWithSelectedItem_GearSetDesign: 'ActiveDesign' is the original name of this property."""

        temp = self.wrapped.ActiveDesign

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_GearSetDesign)(temp) if temp is not None else None

    @active_design.setter
    def active_design(self, value: 'list_with_selected_item.ListWithSelectedItem_GearSetDesign.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_GearSetDesign.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_GearSetDesign.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ActiveDesign = value

    @property
    def maximum_mesh_ratio(self) -> 'float':
        """float: 'MaximumMeshRatio' is the original name of this property."""

        temp = self.wrapped.MaximumMeshRatio

        if temp is None:
            return None

        return temp

    @maximum_mesh_ratio.setter
    def maximum_mesh_ratio(self, value: 'float'):
        self.wrapped.MaximumMeshRatio = float(value) if value else 0.0

    @property
    def maximum_number_of_teeth_in_mesh(self) -> 'int':
        """int: 'MaximumNumberOfTeethInMesh' is the original name of this property."""

        temp = self.wrapped.MaximumNumberOfTeethInMesh

        if temp is None:
            return None

        return temp

    @maximum_number_of_teeth_in_mesh.setter
    def maximum_number_of_teeth_in_mesh(self, value: 'int'):
        self.wrapped.MaximumNumberOfTeethInMesh = int(value) if value else 0

    @property
    def minimum_number_of_teeth_in_mesh(self) -> 'int':
        """int: 'MinimumNumberOfTeethInMesh' is the original name of this property."""

        temp = self.wrapped.MinimumNumberOfTeethInMesh

        if temp is None:
            return None

        return temp

    @minimum_number_of_teeth_in_mesh.setter
    def minimum_number_of_teeth_in_mesh(self, value: 'int'):
        self.wrapped.MinimumNumberOfTeethInMesh = int(value) if value else 0

    @property
    def required_safety_factor_for_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RequiredSafetyFactorForBending' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @required_safety_factor_for_bending.setter
    def required_safety_factor_for_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RequiredSafetyFactorForBending = value

    @property
    def required_safety_factor_for_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RequiredSafetyFactorForContact' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @required_safety_factor_for_contact.setter
    def required_safety_factor_for_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RequiredSafetyFactorForContact = value

    @property
    def required_safety_factor_for_static_bending(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RequiredSafetyFactorForStaticBending' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForStaticBending

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @required_safety_factor_for_static_bending.setter
    def required_safety_factor_for_static_bending(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RequiredSafetyFactorForStaticBending = value

    @property
    def required_safety_factor_for_static_contact(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RequiredSafetyFactorForStaticContact' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForStaticContact

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @required_safety_factor_for_static_contact.setter
    def required_safety_factor_for_static_contact(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RequiredSafetyFactorForStaticContact = value

    @property
    def active_gear_set_design(self) -> '_913.GearSetDesign':
        """GearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _913.GearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to GearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_zerol_bevel_gear_set_design(self) -> '_917.ZerolBevelGearSetDesign':
        """ZerolBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _917.ZerolBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to ZerolBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_worm_gear_set_design(self) -> '_922.WormGearSetDesign':
        """WormGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _922.WormGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to WormGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_straight_bevel_gear_set_design(self) -> '_926.StraightBevelGearSetDesign':
        """StraightBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _926.StraightBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to StraightBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_straight_bevel_diff_gear_set_design(self) -> '_930.StraightBevelDiffGearSetDesign':
        """StraightBevelDiffGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _930.StraightBevelDiffGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to StraightBevelDiffGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_spiral_bevel_gear_set_design(self) -> '_934.SpiralBevelGearSetDesign':
        """SpiralBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _934.SpiralBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to SpiralBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_design(self) -> '_938.KlingelnbergCycloPalloidSpiralBevelGearSetDesign':
        """KlingelnbergCycloPalloidSpiralBevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _938.KlingelnbergCycloPalloidSpiralBevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergCycloPalloidSpiralBevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_design(self) -> '_942.KlingelnbergCycloPalloidHypoidGearSetDesign':
        """KlingelnbergCycloPalloidHypoidGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _942.KlingelnbergCycloPalloidHypoidGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergCycloPalloidHypoidGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_klingelnberg_conical_gear_set_design(self) -> '_946.KlingelnbergConicalGearSetDesign':
        """KlingelnbergConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _946.KlingelnbergConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to KlingelnbergConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_hypoid_gear_set_design(self) -> '_950.HypoidGearSetDesign':
        """HypoidGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _950.HypoidGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to HypoidGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_face_gear_set_design(self) -> '_958.FaceGearSetDesign':
        """FaceGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _958.FaceGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to FaceGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_cylindrical_gear_set_design(self) -> '_990.CylindricalGearSetDesign':
        """CylindricalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _990.CylindricalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to CylindricalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_cylindrical_planetary_gear_set_design(self) -> '_1001.CylindricalPlanetaryGearSetDesign':
        """CylindricalPlanetaryGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _1001.CylindricalPlanetaryGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to CylindricalPlanetaryGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_conical_gear_set_design(self) -> '_1110.ConicalGearSetDesign':
        """ConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _1110.ConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to ConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_concept_gear_set_design(self) -> '_1132.ConceptGearSetDesign':
        """ConceptGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _1132.ConceptGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to ConceptGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_bevel_gear_set_design(self) -> '_1136.BevelGearSetDesign':
        """BevelGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _1136.BevelGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to BevelGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_gear_set_design_of_type_agma_gleason_conical_gear_set_design(self) -> '_1149.AGMAGleasonConicalGearSetDesign':
        """AGMAGleasonConicalGearSetDesign: 'ActiveGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        if _1149.AGMAGleasonConicalGearSetDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_set_design to AGMAGleasonConicalGearSetDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_designs(self) -> 'List[_913.GearSetDesign]':
        """List[GearSetDesign]: 'GearSetDesigns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetDesigns

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_gear_set_design(self, design: '_913.GearSetDesign'):
        """ 'AddGearSetDesign' is the original name of this method.

        Args:
            design (mastapy.gears.gear_designs.GearSetDesign)
        """

        self.wrapped.AddGearSetDesign(design.wrapped if design else None)

    def set_active_gear_set_design(self, gear_set_design: '_913.GearSetDesign'):
        """ 'SetActiveGearSetDesign' is the original name of this method.

        Args:
            gear_set_design (mastapy.gears.gear_designs.GearSetDesign)
        """

        self.wrapped.SetActiveGearSetDesign(gear_set_design.wrapped if gear_set_design else None)
