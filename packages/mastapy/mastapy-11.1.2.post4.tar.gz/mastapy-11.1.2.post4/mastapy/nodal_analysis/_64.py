"""_64.py

FEStiffnessNode
"""


from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS_NODE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEStiffnessNode')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffnessNode',)


class FEStiffnessNode(_0.APIBase):
    """FEStiffnessNode

    This is a mastapy class.
    """

    TYPE = _FE_STIFFNESS_NODE

    def __init__(self, instance_to_wrap: 'FEStiffnessNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_degrees_of_freedom(self) -> 'int':
        """int: 'NumberOfDegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfDegreesOfFreedom

        if temp is None:
            return None

        return temp

    @property
    def position_in_local_coordinate_system(self) -> 'Vector3D':
        """Vector3D: 'PositionInLocalCoordinateSystem' is the original name of this property."""

        temp = self.wrapped.PositionInLocalCoordinateSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @position_in_local_coordinate_system.setter
    def position_in_local_coordinate_system(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.PositionInLocalCoordinateSystem = value

    @property
    def node_index(self) -> 'int':
        """int: 'NodeIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeIndex

        if temp is None:
            return None

        return temp
