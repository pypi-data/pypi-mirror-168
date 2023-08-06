"""_396.py

Iso10300MeshSingleFlankRatingHypoidMethodB2
"""


from mastapy._internal import constructor
from mastapy.gears.rating.iso_10300 import _398
from mastapy._internal.python_net import python_net_import

_ISO_10300_MESH_SINGLE_FLANK_RATING_HYPOID_METHOD_B2 = python_net_import('SMT.MastaAPI.Gears.Rating.Iso10300', 'Iso10300MeshSingleFlankRatingHypoidMethodB2')


__docformat__ = 'restructuredtext en'
__all__ = ('Iso10300MeshSingleFlankRatingHypoidMethodB2',)


class Iso10300MeshSingleFlankRatingHypoidMethodB2(_398.ISO10300MeshSingleFlankRatingMethodB2):
    """Iso10300MeshSingleFlankRatingHypoidMethodB2

    This is a mastapy class.
    """

    TYPE = _ISO_10300_MESH_SINGLE_FLANK_RATING_HYPOID_METHOD_B2

    def __init__(self, instance_to_wrap: 'Iso10300MeshSingleFlankRatingHypoidMethodB2.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length_of_action_from_pinion_tip_to_point_of_load_application(self) -> 'float':
        """float: 'LengthOfActionFromPinionTipToPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionFromPinionTipToPointOfLoadApplication

        if temp is None:
            return None

        return temp

    @property
    def length_of_action_from_wheel_tip_to_point_of_load_application(self) -> 'float':
        """float: 'LengthOfActionFromWheelTipToPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionFromWheelTipToPointOfLoadApplication

        if temp is None:
            return None

        return temp

    @property
    def lengthwise_load_sharing_factor(self) -> 'float':
        """float: 'LengthwiseLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthwiseLoadSharingFactor

        if temp is None:
            return None

        return temp

    @property
    def pinion_length_of_action_point_of_load_application(self) -> 'float':
        """float: 'PinionLengthOfActionPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionLengthOfActionPointOfLoadApplication

        if temp is None:
            return None

        return temp

    @property
    def profile_load_sharing_factor(self) -> 'float':
        """float: 'ProfileLoadSharingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileLoadSharingFactor

        if temp is None:
            return None

        return temp

    @property
    def wheel_length_of_action_point_of_load_application(self) -> 'float':
        """float: 'WheelLengthOfActionPointOfLoadApplication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelLengthOfActionPointOfLoadApplication

        if temp is None:
            return None

        return temp
