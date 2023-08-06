"""_119.py

NodeScalarState
"""


from mastapy.nodal_analysis.states import _120
from mastapy._internal.python_net import python_net_import

_NODE_SCALAR_STATE = python_net_import('SMT.MastaAPI.NodalAnalysis.States', 'NodeScalarState')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeScalarState',)


class NodeScalarState(_120.NodeVectorState):
    """NodeScalarState

    This is a mastapy class.
    """

    TYPE = _NODE_SCALAR_STATE

    def __init__(self, instance_to_wrap: 'NodeScalarState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
