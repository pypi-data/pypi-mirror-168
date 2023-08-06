"""_95.py

VelocityInputComponent
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.varying_input_components import _89
from mastapy._internal.python_net import python_net_import

_VELOCITY_INPUT_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.VaryingInputComponents', 'VelocityInputComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('VelocityInputComponent',)


class VelocityInputComponent(_89.AbstractVaryingInputComponent):
    """VelocityInputComponent

    This is a mastapy class.
    """

    TYPE = _VELOCITY_INPUT_COMPONENT

    def __init__(self, instance_to_wrap: 'VelocityInputComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def velocity(self) -> 'float':
        """float: 'Velocity' is the original name of this property."""

        temp = self.wrapped.Velocity

        if temp is None:
            return None

        return temp

    @velocity.setter
    def velocity(self, value: 'float'):
        self.wrapped.Velocity = float(value) if value else 0.0
