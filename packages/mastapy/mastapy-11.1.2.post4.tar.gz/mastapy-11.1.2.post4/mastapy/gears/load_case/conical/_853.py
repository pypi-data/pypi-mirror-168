"""_853.py

ConicalMeshLoadCase
"""


from mastapy.gears.gear_designs.conical import _1104, _1114
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.load_case import _841
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.Gears.LoadCase.Conical', 'ConicalMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshLoadCase',)


class ConicalMeshLoadCase(_841.MeshLoadCase):
    """ConicalMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'ConicalMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_1104.ActiveConicalFlank':
        """ActiveConicalFlank: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1104.ActiveConicalFlank)(value) if value is not None else None

    @property
    def use_user_specified_misalignments_in_tca(self) -> 'bool':
        """bool: 'UseUserSpecifiedMisalignmentsInTCA' is the original name of this property."""

        temp = self.wrapped.UseUserSpecifiedMisalignmentsInTCA

        if temp is None:
            return None

        return temp

    @use_user_specified_misalignments_in_tca.setter
    def use_user_specified_misalignments_in_tca(self, value: 'bool'):
        self.wrapped.UseUserSpecifiedMisalignmentsInTCA = bool(value) if value else False

    @property
    def mesh_node_misalignments_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsPinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_node_misalignments_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_node_misalignments_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MeshNodeMisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshNodeMisalignmentsWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsPinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsPinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_pinion(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodePinion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_total(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeTotal

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def misalignments_with_respect_to_cross_point_using_reference_fe_substructure_node_wheel(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MisalignmentsWithRespectToCrossPointUsingReferenceFESubstructureNodeWheel

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def user_specified_misalignments(self) -> '_1114.ConicalMeshMisalignments':
        """ConicalMeshMisalignments: 'UserSpecifiedMisalignments' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UserSpecifiedMisalignments

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
