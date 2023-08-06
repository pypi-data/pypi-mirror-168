"""_944.py

KlingelnbergConicalGearDesign
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import
from mastapy.gears.materials import _567
from mastapy.gears.gear_designs.conical import _1108

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_KLINGELNBERG_CONICAL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.KlingelnbergConical', 'KlingelnbergConicalGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergConicalGearDesign',)


class KlingelnbergConicalGearDesign(_1108.ConicalGearDesign):
    """KlingelnbergConicalGearDesign

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CONICAL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'KlingelnbergConicalGearDesign.TYPE'):
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
    def cutter_edge_radius(self) -> 'float':
        """float: 'CutterEdgeRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterEdgeRadius

        if temp is None:
            return None

        return temp

    @property
    def flank_roughness_rz(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FlankRoughnessRZ' is the original name of this property."""

        temp = self.wrapped.FlankRoughnessRZ

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @flank_roughness_rz.setter
    def flank_roughness_rz(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FlankRoughnessRZ = value

    @property
    def material(self) -> 'str':
        """str: 'Material' is the original name of this property."""

        temp = self.wrapped.Material.SelectedItemName

        if temp is None:
            return None

        return temp

    @material.setter
    def material(self, value: 'str'):
        self.wrapped.Material.SetSelectedItem(str(value) if value else '')

    @property
    def pitch_cone_angle(self) -> 'float':
        """float: 'PitchConeAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchConeAngle

        if temp is None:
            return None

        return temp

    @property
    def relative_sensitivity_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RelativeSensitivityFactor' is the original name of this property."""

        temp = self.wrapped.RelativeSensitivityFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @relative_sensitivity_factor.setter
    def relative_sensitivity_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RelativeSensitivityFactor = value

    @property
    def stress_correction_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'StressCorrectionFactor' is the original name of this property."""

        temp = self.wrapped.StressCorrectionFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @stress_correction_factor.setter
    def stress_correction_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.StressCorrectionFactor = value

    @property
    def tooth_form_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ToothFormFactor' is the original name of this property."""

        temp = self.wrapped.ToothFormFactor

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @tooth_form_factor.setter
    def tooth_form_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ToothFormFactor = value

    @property
    def klingelnberg_cyclo_palloid_gear_material(self) -> '_567.KlingelnbergCycloPalloidConicalGearMaterial':
        """KlingelnbergCycloPalloidConicalGearMaterial: 'KlingelnbergCycloPalloidGearMaterial' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidGearMaterial

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
