"""_553.py

BevelGearMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.materials import _574, _560
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'BevelGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearMaterial',)


class BevelGearMaterial(_560.GearMaterial):
    """BevelGearMaterial

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_MATERIAL

    def __init__(self, instance_to_wrap: 'BevelGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_bending_stress(self) -> 'float':
        """float: 'AllowableBendingStress' is the original name of this property."""

        temp = self.wrapped.AllowableBendingStress

        if temp is None:
            return None

        return temp

    @allowable_bending_stress.setter
    def allowable_bending_stress(self, value: 'float'):
        self.wrapped.AllowableBendingStress = float(value) if value else 0.0

    @property
    def allowable_contact_stress(self) -> 'float':
        """float: 'AllowableContactStress' is the original name of this property."""

        temp = self.wrapped.AllowableContactStress

        if temp is None:
            return None

        return temp

    @allowable_contact_stress.setter
    def allowable_contact_stress(self, value: 'float'):
        self.wrapped.AllowableContactStress = float(value) if value else 0.0

    @property
    def sn_curve_definition(self) -> '_574.SNCurveDefinition':
        """SNCurveDefinition: 'SNCurveDefinition' is the original name of this property."""

        temp = self.wrapped.SNCurveDefinition

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_574.SNCurveDefinition)(value) if value is not None else None

    @sn_curve_definition.setter
    def sn_curve_definition(self, value: '_574.SNCurveDefinition'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SNCurveDefinition = value

    @property
    def thermal_constant(self) -> 'float':
        """float: 'ThermalConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThermalConstant

        if temp is None:
            return None

        return temp
