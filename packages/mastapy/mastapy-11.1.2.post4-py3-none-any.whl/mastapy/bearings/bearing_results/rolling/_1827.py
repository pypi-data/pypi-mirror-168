"""_1827.py

RingForceAndDisplacement
"""


from mastapy._internal import constructor
from mastapy.math_utility.measured_vectors import _1371
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RING_FORCE_AND_DISPLACEMENT = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'RingForceAndDisplacement')


__docformat__ = 'restructuredtext en'
__all__ = ('RingForceAndDisplacement',)


class RingForceAndDisplacement(_0.APIBase):
    """RingForceAndDisplacement

    This is a mastapy class.
    """

    TYPE = _RING_FORCE_AND_DISPLACEMENT

    def __init__(self, instance_to_wrap: 'RingForceAndDisplacement.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def magnitude_of_misalignment_normal_to_load_direction(self) -> 'float':
        """float: 'MagnitudeOfMisalignmentNormalToLoadDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MagnitudeOfMisalignmentNormalToLoadDirection

        if temp is None:
            return None

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return None

        return temp

    @property
    def displacement(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'Displacement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Displacement

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def force(self) -> '_1371.VectorWithLinearAndAngularComponents':
        """VectorWithLinearAndAngularComponents: 'Force' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Force

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
