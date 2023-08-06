"""_206.py

CMSNodeGroup
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.dev_tools_analyses import _179
from mastapy._internal.python_net import python_net_import

_CMS_NODE_GROUP = python_net_import('SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis', 'CMSNodeGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('CMSNodeGroup',)


class CMSNodeGroup(_179.NodeGroup):
    """CMSNodeGroup

    This is a mastapy class.
    """

    TYPE = _CMS_NODE_GROUP

    def __init__(self, instance_to_wrap: 'CMSNodeGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def show_nvh_results_at_these_nodes(self) -> 'bool':
        """bool: 'ShowNVHResultsAtTheseNodes' is the original name of this property."""

        temp = self.wrapped.ShowNVHResultsAtTheseNodes

        if temp is None:
            return None

        return temp

    @show_nvh_results_at_these_nodes.setter
    def show_nvh_results_at_these_nodes(self, value: 'bool'):
        self.wrapped.ShowNVHResultsAtTheseNodes = bool(value) if value else False

    def create_element_face_group(self):
        """ 'CreateElementFaceGroup' is the original name of this method."""

        self.wrapped.CreateElementFaceGroup()
