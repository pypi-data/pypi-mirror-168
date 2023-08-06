"""_1270.py

RingPinsMaterialDatabase
"""


from mastapy.materials import _246
from mastapy.cycloidal import _1269
from mastapy._internal.python_net import python_net_import

_RING_PINS_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Cycloidal', 'RingPinsMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsMaterialDatabase',)


class RingPinsMaterialDatabase(_246.MaterialDatabase['_1269.RingPinsMaterial']):
    """RingPinsMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _RING_PINS_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'RingPinsMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
