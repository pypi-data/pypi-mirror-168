"""_1259.py

ContactSpecification
"""


from mastapy._internal import constructor, conversion
from mastapy._math.vector_2d import Vector2D
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONTACT_SPECIFICATION = python_net_import('SMT.MastaAPI.Cycloidal', 'ContactSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('ContactSpecification',)


class ContactSpecification(_0.APIBase):
    """ContactSpecification

    This is a mastapy class.
    """

    TYPE = _CONTACT_SPECIFICATION

    def __init__(self, instance_to_wrap: 'ContactSpecification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clearance(self) -> 'float':
        """float: 'Clearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clearance

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
    def contact_line_direction(self) -> 'Vector2D':
        """Vector2D: 'ContactLineDirection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLineDirection

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def contact_line_point_1(self) -> 'Vector2D':
        """Vector2D: 'ContactLinePoint1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLinePoint1

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def contact_line_point_2(self) -> 'Vector2D':
        """Vector2D: 'ContactLinePoint2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLinePoint2

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def contact_point(self) -> 'Vector2D':
        """Vector2D: 'ContactPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactPoint

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @property
    def estimate_contact_point(self) -> 'Vector2D':
        """Vector2D: 'EstimateContactPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EstimateContactPoint

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value
