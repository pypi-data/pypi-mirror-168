"""_2145.py

GearMeshingOptions
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.fe_model import _1153
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MESHING_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.FE', 'GearMeshingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshingOptions',)


class GearMeshingOptions(_0.APIBase):
    """GearMeshingOptions

    This is a mastapy class.
    """

    TYPE = _GEAR_MESHING_OPTIONS

    def __init__(self, instance_to_wrap: 'GearMeshingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Diameter' is the original name of this property."""

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @diameter.setter
    def diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Diameter = value

    @property
    def mesh_teeth(self) -> 'bool':
        """bool: 'MeshTeeth' is the original name of this property."""

        temp = self.wrapped.MeshTeeth

        if temp is None:
            return None

        return temp

    @mesh_teeth.setter
    def mesh_teeth(self, value: 'bool'):
        self.wrapped.MeshTeeth = bool(value) if value else False

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def offset_of_gear_centre_calculated_from_fe(self) -> 'str':
        """str: 'OffsetOfGearCentreCalculatedFromFE' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OffsetOfGearCentreCalculatedFromFE

        if temp is None:
            return None

        return temp

    @property
    def element_settings(self) -> '_1153.GearMeshingElementOptions':
        """GearMeshingElementOptions: 'ElementSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElementSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
