"""_2151.py

NodeGroupWithSelection
"""


from mastapy.system_model.fe import _2128
from mastapy.nodal_analysis.component_mode_synthesis import _206
from mastapy._internal.python_net import python_net_import

_NODE_GROUP_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'NodeGroupWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('NodeGroupWithSelection',)


class NodeGroupWithSelection(_2128.FEEntityGroupWithSelection['_206.CMSNodeGroup', 'int']):
    """NodeGroupWithSelection

    This is a mastapy class.
    """

    TYPE = _NODE_GROUP_WITH_SELECTION

    def __init__(self, instance_to_wrap: 'NodeGroupWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
