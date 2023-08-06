"""_481.py

ISO63362006MeshSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.cylindrical.iso6336 import _487
from mastapy._internal.python_net import python_net_import

_ISO63362006_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ISO63362006MeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO63362006MeshSingleFlankRating',)


class ISO63362006MeshSingleFlankRating(_487.ISO6336AbstractMetalMeshSingleFlankRating):
    """ISO63362006MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _ISO63362006_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'ISO63362006MeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def deep_tooth_factor(self) -> 'float':
        """float: 'DeepToothFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DeepToothFactor

        if temp is None:
            return None

        return temp

    @property
    def dynamic_factor_source(self) -> 'str':
        """str: 'DynamicFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicFactorSource

        if temp is None:
            return None

        return temp

    @property
    def helix_angle_factor_contact(self) -> 'float':
        """float: 'HelixAngleFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleFactorContact

        if temp is None:
            return None

        return temp

    @property
    def mesh_stiffness_face(self) -> 'float':
        """float: 'MeshStiffnessFace' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshStiffnessFace

        if temp is None:
            return None

        return temp

    @property
    def mesh_stiffness_transverse(self) -> 'float':
        """float: 'MeshStiffnessTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshStiffnessTransverse

        if temp is None:
            return None

        return temp

    @property
    def rating_standard_name(self) -> 'str':
        """str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingStandardName

        if temp is None:
            return None

        return temp

    @property
    def transverse_load_factor_bending(self) -> 'float':
        """float: 'TransverseLoadFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadFactorBending

        if temp is None:
            return None

        return temp
