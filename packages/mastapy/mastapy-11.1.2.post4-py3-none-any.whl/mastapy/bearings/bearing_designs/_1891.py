"""_1891.py

LinearBearing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1647
from mastapy.bearings.bearing_designs import _1888
from mastapy._internal.python_net import python_net_import

_LINEAR_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns', 'LinearBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('LinearBearing',)


class LinearBearing(_1888.BearingDesign):
    """LinearBearing

    This is a mastapy class.
    """

    TYPE = _LINEAR_BEARING

    def __init__(self, instance_to_wrap: 'LinearBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_stiffness(self) -> 'float':
        """float: 'AxialStiffness' is the original name of this property."""

        temp = self.wrapped.AxialStiffness

        if temp is None:
            return None

        return temp

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'float'):
        self.wrapped.AxialStiffness = float(value) if value else 0.0

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property."""

        temp = self.wrapped.Bore

        if temp is None:
            return None

        return temp

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value else 0.0

    @property
    def outer_diameter(self) -> 'float':
        """float: 'OuterDiameter' is the original name of this property."""

        temp = self.wrapped.OuterDiameter

        if temp is None:
            return None

        return temp

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value else 0.0

    @property
    def radial_stiffness(self) -> 'float':
        """float: 'RadialStiffness' is the original name of this property."""

        temp = self.wrapped.RadialStiffness

        if temp is None:
            return None

        return temp

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'float'):
        self.wrapped.RadialStiffness = float(value) if value else 0.0

    @property
    def stiffness_options(self) -> '_1647.BearingStiffnessMatrixOption':
        """BearingStiffnessMatrixOption: 'StiffnessOptions' is the original name of this property."""

        temp = self.wrapped.StiffnessOptions

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1647.BearingStiffnessMatrixOption)(value) if value is not None else None

    @stiffness_options.setter
    def stiffness_options(self, value: '_1647.BearingStiffnessMatrixOption'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StiffnessOptions = value

    @property
    def tilt_stiffness(self) -> 'float':
        """float: 'TiltStiffness' is the original name of this property."""

        temp = self.wrapped.TiltStiffness

        if temp is None:
            return None

        return temp

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'float'):
        self.wrapped.TiltStiffness = float(value) if value else 0.0
