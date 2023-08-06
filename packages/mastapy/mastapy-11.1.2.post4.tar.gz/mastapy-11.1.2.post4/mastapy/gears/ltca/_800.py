"""_800.py

GearBendingStiffnessNode
"""


from mastapy.gears.ltca import _814
from mastapy._internal.python_net import python_net_import

_GEAR_BENDING_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearBendingStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('GearBendingStiffnessNode',)


class GearBendingStiffnessNode(_814.GearStiffnessNode):
    """GearBendingStiffnessNode

    This is a mastapy class.
    """

    TYPE = _GEAR_BENDING_STIFFNESS_NODE

    def __init__(self, instance_to_wrap: 'GearBendingStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
