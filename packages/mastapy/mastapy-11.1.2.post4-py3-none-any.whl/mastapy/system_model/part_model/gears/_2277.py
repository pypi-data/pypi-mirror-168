"""_2277.py

FaceGear
"""


from mastapy.system_model.part_model.gears import _2280, _2279
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.face import _952, _957, _960
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGear',)


class FaceGear(_2279.Gear):
    """FaceGear

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR

    def __init__(self, instance_to_wrap: 'FaceGear.TYPE'):
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
    def active_gear_design(self) -> '_952.FaceGearDesign':
        """FaceGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveGearDesign

        if temp is None:
            return None

        if _952.FaceGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast active_gear_design to FaceGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gear_design(self) -> '_952.FaceGearDesign':
        """FaceGearDesign: 'FaceGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearDesign

        if temp is None:
            return None

        if _952.FaceGearDesign.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast face_gear_design to FaceGearDesign. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
