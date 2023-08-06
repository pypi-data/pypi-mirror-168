"""_820.py

CylindricalGearContactStiffnessNode
"""


from mastapy.gears.ltca import _802
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_CONTACT_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.Gears.LTCA.Cylindrical', 'CylindricalGearContactStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearContactStiffnessNode',)


class CylindricalGearContactStiffnessNode(_802.GearContactStiffnessNode):
    """CylindricalGearContactStiffnessNode

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_CONTACT_STIFFNESS_NODE

    def __init__(self, instance_to_wrap: 'CylindricalGearContactStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
