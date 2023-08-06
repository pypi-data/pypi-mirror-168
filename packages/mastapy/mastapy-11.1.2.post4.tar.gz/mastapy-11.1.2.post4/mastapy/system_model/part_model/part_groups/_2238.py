"""_2238.py

ConcentricPartGroupParallelToThis
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.part_groups import _2236, _2237, _2240
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.PartGroups', 'ConcentricPartGroupParallelToThis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConcentricPartGroupParallelToThis',)


class ConcentricPartGroupParallelToThis(_0.APIBase):
    """ConcentricPartGroupParallelToThis

    This is a mastapy class.
    """

    TYPE = _CONCENTRIC_PART_GROUP_PARALLEL_TO_THIS

    def __init__(self, instance_to_wrap: 'ConcentricPartGroupParallelToThis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CentreDistance

        if temp is None:
            return None

        return temp

    @property
    def parallel_group(self) -> '_2236.ConcentricOrParallelPartGroup':
        """ConcentricOrParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParallelGroup

        if temp is None:
            return None

        if _2236.ConcentricOrParallelPartGroup.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast parallel_group to ConcentricOrParallelPartGroup. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parallel_group_of_type_concentric_part_group(self) -> '_2237.ConcentricPartGroup':
        """ConcentricPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParallelGroup

        if temp is None:
            return None

        if _2237.ConcentricPartGroup.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast parallel_group to ConcentricPartGroup. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parallel_group_of_type_parallel_part_group(self) -> '_2240.ParallelPartGroup':
        """ParallelPartGroup: 'ParallelGroup' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParallelGroup

        if temp is None:
            return None

        if _2240.ParallelPartGroup.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast parallel_group to ParallelPartGroup. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
