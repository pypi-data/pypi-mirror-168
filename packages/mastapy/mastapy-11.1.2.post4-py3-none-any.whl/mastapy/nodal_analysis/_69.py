"""_69.py

LinearDampingConnectionProperties
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis import _43
from mastapy._internal.python_net import python_net_import

_LINEAR_DAMPING_CONNECTION_PROPERTIES = python_net_import('SMT.MastaAPI.NodalAnalysis', 'LinearDampingConnectionProperties')


__docformat__ = 'restructuredtext en'
__all__ = ('LinearDampingConnectionProperties',)


class LinearDampingConnectionProperties(_43.AbstractLinearConnectionProperties):
    """LinearDampingConnectionProperties

    This is a mastapy class.
    """

    TYPE = _LINEAR_DAMPING_CONNECTION_PROPERTIES

    def __init__(self, instance_to_wrap: 'LinearDampingConnectionProperties.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_damping(self) -> 'float':
        """float: 'AxialDamping' is the original name of this property."""

        temp = self.wrapped.AxialDamping

        if temp is None:
            return None

        return temp

    @axial_damping.setter
    def axial_damping(self, value: 'float'):
        self.wrapped.AxialDamping = float(value) if value else 0.0

    @property
    def radial_damping(self) -> 'float':
        """float: 'RadialDamping' is the original name of this property."""

        temp = self.wrapped.RadialDamping

        if temp is None:
            return None

        return temp

    @radial_damping.setter
    def radial_damping(self, value: 'float'):
        self.wrapped.RadialDamping = float(value) if value else 0.0

    @property
    def tilt_damping(self) -> 'float':
        """float: 'TiltDamping' is the original name of this property."""

        temp = self.wrapped.TiltDamping

        if temp is None:
            return None

        return temp

    @tilt_damping.setter
    def tilt_damping(self, value: 'float'):
        self.wrapped.TiltDamping = float(value) if value else 0.0

    @property
    def torsional_damping(self) -> 'float':
        """float: 'TorsionalDamping' is the original name of this property."""

        temp = self.wrapped.TorsionalDamping

        if temp is None:
            return None

        return temp

    @torsional_damping.setter
    def torsional_damping(self, value: 'float'):
        self.wrapped.TorsionalDamping = float(value) if value else 0.0
