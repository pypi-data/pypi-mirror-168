"""_120.py

NodeVectorState
"""


from mastapy.nodal_analysis.states import _118
from mastapy._internal.python_net import python_net_import

_NODE_VECTOR_STATE = python_net_import('SMT.MastaAPI.NodalAnalysis.States', 'NodeVectorState')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeVectorState',)


class NodeVectorState(_118.EntityVectorState):
    """NodeVectorState

    This is a mastapy class.
    """

    TYPE = _NODE_VECTOR_STATE

    def __init__(self, instance_to_wrap: 'NodeVectorState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
