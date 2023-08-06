"""_1267.py

NamedDiscPhase
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NAMED_DISC_PHASE = python_net_import('SMT.MastaAPI.Cycloidal', 'NamedDiscPhase')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedDiscPhase',)


class NamedDiscPhase(_0.APIBase):
    """NamedDiscPhase

    This is a mastapy class.
    """

    TYPE = _NAMED_DISC_PHASE

    def __init__(self, instance_to_wrap: 'NamedDiscPhase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def disc_phase_angle(self) -> 'float':
        """float: 'DiscPhaseAngle' is the original name of this property."""

        temp = self.wrapped.DiscPhaseAngle

        if temp is None:
            return None

        return temp

    @disc_phase_angle.setter
    def disc_phase_angle(self, value: 'float'):
        self.wrapped.DiscPhaseAngle = float(value) if value else 0.0
