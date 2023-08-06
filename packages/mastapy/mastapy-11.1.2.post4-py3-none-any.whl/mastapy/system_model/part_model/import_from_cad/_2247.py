"""_2247.py

CylindricalGearFromCAD
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy.system_model.part_model.gears import _2275, _2274
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.geometry.two_d import _284
from mastapy.system_model.part_model.import_from_cad import _2253
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'CylindricalGearFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFromCAD',)


class CylindricalGearFromCAD(_2253.MountableComponentFromCAD):
    """CylindricalGearFromCAD

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FROM_CAD

    def __init__(self, instance_to_wrap: 'CylindricalGearFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cad_drawing_diameter(self) -> 'float':
        """float: 'CADDrawingDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CADDrawingDiameter

        if temp is None:
            return None

        return temp

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property."""

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def existing_gear_set(self) -> 'list_with_selected_item.ListWithSelectedItem_CylindricalGearSet':
        """list_with_selected_item.ListWithSelectedItem_CylindricalGearSet: 'ExistingGearSet' is the original name of this property."""

        temp = self.wrapped.ExistingGearSet

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_CylindricalGearSet)(temp) if temp is not None else None

    @existing_gear_set.setter
    def existing_gear_set(self, value: 'list_with_selected_item.ListWithSelectedItem_CylindricalGearSet.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearSet.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalGearSet.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.ExistingGearSet = value

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value else 0.0

    @property
    def gear_set_name(self) -> 'str':
        """str: 'GearSetName' is the original name of this property."""

        temp = self.wrapped.GearSetName

        if temp is None:
            return None

        return temp

    @gear_set_name.setter
    def gear_set_name(self, value: 'str'):
        self.wrapped.GearSetName = str(value) if value else ''

    @property
    def helix_angle(self) -> 'float':
        """float: 'HelixAngle' is the original name of this property."""

        temp = self.wrapped.HelixAngle

        if temp is None:
            return None

        return temp

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value else 0.0

    @property
    def internal_external(self) -> '_284.InternalExternalType':
        """InternalExternalType: 'InternalExternal' is the original name of this property."""

        temp = self.wrapped.InternalExternal

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_284.InternalExternalType)(value) if value is not None else None

    @internal_external.setter
    def internal_external(self, value: '_284.InternalExternalType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.InternalExternal = value

    @property
    def meshing_gear(self) -> 'list_with_selected_item.ListWithSelectedItem_CylindricalGear':
        """list_with_selected_item.ListWithSelectedItem_CylindricalGear: 'MeshingGear' is the original name of this property."""

        temp = self.wrapped.MeshingGear

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_CylindricalGear)(temp) if temp is not None else None

    @meshing_gear.setter
    def meshing_gear(self, value: 'list_with_selected_item.ListWithSelectedItem_CylindricalGear.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_CylindricalGear.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_CylindricalGear.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.MeshingGear = value

    @property
    def normal_module(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'NormalModule' is the original name of this property."""

        temp = self.wrapped.NormalModule

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @normal_module.setter
    def normal_module(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.NormalModule = value

    @property
    def normal_pressure_angle(self) -> 'float':
        """float: 'NormalPressureAngle' is the original name of this property."""

        temp = self.wrapped.NormalPressureAngle

        if temp is None:
            return None

        return temp

    @normal_pressure_angle.setter
    def normal_pressure_angle(self, value: 'float'):
        self.wrapped.NormalPressureAngle = float(value) if value else 0.0

    @property
    def number_of_teeth(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'NumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.NumberOfTeeth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else None

    @number_of_teeth.setter
    def number_of_teeth(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.NumberOfTeeth = value

    @property
    def root_diameter(self) -> 'float':
        """float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootDiameter

        if temp is None:
            return None

        return temp

    @property
    def tip_diameter(self) -> 'float':
        """float: 'TipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipDiameter

        if temp is None:
            return None

        return temp
