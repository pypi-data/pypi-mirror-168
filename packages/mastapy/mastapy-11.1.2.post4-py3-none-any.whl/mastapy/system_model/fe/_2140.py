"""_2140.py

FESubstructureWithSelection
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.fe import (
    _2133, _2126, _2151, _2111
)
from mastapy._internal.python_net import python_net_import

_FE_SUBSTRUCTURE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('FESubstructureWithSelection',)


class FESubstructureWithSelection(_2111.BaseFEWithSelection):
    """FESubstructureWithSelection

    This is a mastapy class.
    """

    TYPE = _FE_SUBSTRUCTURE_WITH_SELECTION

    def __init__(self, instance_to_wrap: 'FESubstructureWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def selected_nodes(self) -> 'str':
        """str: 'SelectedNodes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedNodes

        if temp is None:
            return None

        return temp

    @property
    def fe_substructure(self) -> '_2133.FESubstructure':
        """FESubstructure: 'FESubstructure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FESubstructure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def element_face_groups(self) -> 'List[_2126.ElementFaceGroupWithSelection]':
        """List[ElementFaceGroupWithSelection]: 'ElementFaceGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElementFaceGroups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def node_groups(self) -> 'List[_2151.NodeGroupWithSelection]':
        """List[NodeGroupWithSelection]: 'NodeGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NodeGroups

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def create_condensation_node_connected_to_current_selection(self):
        """ 'CreateCondensationNodeConnectedToCurrentSelection' is the original name of this method."""

        self.wrapped.CreateCondensationNodeConnectedToCurrentSelection()

    def create_element_face_group(self):
        """ 'CreateElementFaceGroup' is the original name of this method."""

        self.wrapped.CreateElementFaceGroup()

    def create_node_group(self):
        """ 'CreateNodeGroup' is the original name of this method."""

        self.wrapped.CreateNodeGroup()

    def ground_selected_faces(self):
        """ 'GroundSelectedFaces' is the original name of this method."""

        self.wrapped.GroundSelectedFaces()

    def remove_grounding_on_selected_faces(self):
        """ 'RemoveGroundingOnSelectedFaces' is the original name of this method."""

        self.wrapped.RemoveGroundingOnSelectedFaces()
