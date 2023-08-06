"""_270.py

IndependentResistiveTorque
"""


from mastapy._internal import constructor
from mastapy.materials.efficiency import _277
from mastapy._internal.python_net import python_net_import

_INDEPENDENT_RESISTIVE_TORQUE = python_net_import('SMT.MastaAPI.Materials.Efficiency', 'IndependentResistiveTorque')


__docformat__ = 'restructuredtext en'
__all__ = ('IndependentResistiveTorque',)


class IndependentResistiveTorque(_277.ResistiveTorque):
    """IndependentResistiveTorque

    This is a mastapy class.
    """

    TYPE = _INDEPENDENT_RESISTIVE_TORQUE

    def __init__(self, instance_to_wrap: 'IndependentResistiveTorque.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_dependent_resistive_torque(self) -> 'float':
        """float: 'LoadDependentResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDependentResistiveTorque

        if temp is None:
            return None

        return temp

    @property
    def speed_dependent_resistive_torque(self) -> 'float':
        """float: 'SpeedDependentResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedDependentResistiveTorque

        if temp is None:
            return None

        return temp
