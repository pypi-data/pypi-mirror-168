"""_2146.py

IndependentMastaCreatedCondensationNode
"""


from mastapy.nodal_analysis.dev_tools_analyses import _181
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.fe import _2135
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_INDEPENDENT_MASTA_CREATED_CONDENSATION_NODE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'IndependentMastaCreatedCondensationNode')


__docformat__ = 'restructuredtext en'
__all__ = ('IndependentMastaCreatedCondensationNode',)


class IndependentMastaCreatedCondensationNode(_0.APIBase):
    """IndependentMastaCreatedCondensationNode

    This is a mastapy class.
    """

    TYPE = _INDEPENDENT_MASTA_CREATED_CONDENSATION_NODE

    def __init__(self, instance_to_wrap: 'IndependentMastaCreatedCondensationNode.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def rigid_coupling_type(self) -> '_181.RigidCouplingType':
        """RigidCouplingType: 'RigidCouplingType' is the original name of this property."""

        temp = self.wrapped.RigidCouplingType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_181.RigidCouplingType)(value) if value is not None else None

    @rigid_coupling_type.setter
    def rigid_coupling_type(self, value: '_181.RigidCouplingType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RigidCouplingType = value

    @property
    def fe_substructure_node(self) -> '_2135.FESubstructureNode':
        """FESubstructureNode: 'FESubstructureNode' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FESubstructureNode

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def node_position(self) -> 'Vector3D':
        """Vector3D: 'NodePosition' is the original name of this property."""

        temp = self.wrapped.NodePosition

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @node_position.setter
    def node_position(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.NodePosition = value

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()
