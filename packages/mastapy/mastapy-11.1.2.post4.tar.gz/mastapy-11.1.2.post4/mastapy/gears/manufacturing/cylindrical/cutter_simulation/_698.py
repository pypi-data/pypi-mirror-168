"""_698.py

CylindricalCutterSimulatableGear
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.geometry.two_d import _284
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_CUTTER_SIMULATABLE_GEAR = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalCutterSimulatableGear')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalCutterSimulatableGear',)


class CylindricalCutterSimulatableGear(_0.APIBase):
    """CylindricalCutterSimulatableGear

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_CUTTER_SIMULATABLE_GEAR

    def __init__(self, instance_to_wrap: 'CylindricalCutterSimulatableGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @property
    def generating_addendum_modification_factor(self) -> 'float':
        """float: 'GeneratingAddendumModificationFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeneratingAddendumModificationFactor

        if temp is None:
            return None

        return temp

    @property
    def helix_angle(self) -> 'float':
        """float: 'HelixAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngle

        if temp is None:
            return None

        return temp

    @property
    def internal_external(self) -> '_284.InternalExternalType':
        """InternalExternalType: 'InternalExternal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InternalExternal

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_284.InternalExternalType)(value) if value is not None else None

    @property
    def is_left_handed(self) -> 'bool':
        """bool: 'IsLeftHanded' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsLeftHanded

        if temp is None:
            return None

        return temp

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
    def normal_module(self) -> 'float':
        """float: 'NormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalModule

        if temp is None:
            return None

        return temp

    @property
    def normal_pressure_angle(self) -> 'float':
        """float: 'NormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalPressureAngle

        if temp is None:
            return None

        return temp

    @property
    def normal_thickness(self) -> 'float':
        """float: 'NormalThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalThickness

        if temp is None:
            return None

        return temp

    @property
    def number_of_teeth_unsigned(self) -> 'float':
        """float: 'NumberOfTeethUnsigned' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfTeethUnsigned

        if temp is None:
            return None

        return temp

    @property
    def reference_diameter(self) -> 'float':
        """float: 'ReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceDiameter

        if temp is None:
            return None

        return temp

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
    def root_form_diameter(self) -> 'float':
        """float: 'RootFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootFormDiameter

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

    @property
    def tip_form_diameter(self) -> 'float':
        """float: 'TipFormDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipFormDiameter

        if temp is None:
            return None

        return temp
