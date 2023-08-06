"""_2270.py

ConceptGear
"""


from mastapy.system_model.part_model.gears import _2280, _2279
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.concept import _1130
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGear',)


class ConceptGear(_2279.Gear):
    """ConceptGear

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR

    def __init__(self, instance_to_wrap: 'ConceptGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def orientation(self) -> '_2280.GearOrientations':
        """GearOrientations: 'Orientation' is the original name of this property."""

        temp = self.wrapped.Orientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2280.GearOrientations)(value) if value is not None else None

    @orientation.setter
    def orientation(self, value: '_2280.GearOrientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def active_gear_design(self) -> '_1130.ConceptGearDesign':
        """ConceptGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def concept_gear_design(self) -> '_1130.ConceptGearDesign':
        """ConceptGearDesign: 'ConceptGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
