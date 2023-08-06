"""_1366.py

AbstractForceAndDisplacementResults
"""


from mastapy._internal import constructor, conversion
from mastapy.math_utility.measured_vectors import _1371
from mastapy._math.vector_3d import Vector3D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_FORCE_AND_DISPLACEMENT_RESULTS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredVectors', 'AbstractForceAndDisplacementResults')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractForceAndDisplacementResults',)


class AbstractForceAndDisplacementResults(_0.APIBase):
    """AbstractForceAndDisplacementResults

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_FORCE_AND_DISPLACEMENT_RESULTS

    def __init__(self, instance_to_wrap: 'AbstractForceAndDisplacementResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def node(self) -> 'str':
        """str: 'Node' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Node

        if temp is None:
            return None

        return temp

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

    @property
    def location(self) -> 'Vector3D':
        """Vector3D: 'Location' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Location

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value
