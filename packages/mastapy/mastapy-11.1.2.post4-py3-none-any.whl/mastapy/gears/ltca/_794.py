"""_794.py

CylindricalGearFilletNodeStressResults
"""


from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy.gears.ltca import _803
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'CylindricalGearFilletNodeStressResults')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFilletNodeStressResults',)


class CylindricalGearFilletNodeStressResults(_803.GearFilletNodeStressResults):
    """CylindricalGearFilletNodeStressResults

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FILLET_NODE_STRESS_RESULTS

    def __init__(self, instance_to_wrap: 'CylindricalGearFilletNodeStressResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter(self) -> 'float':
        """float: 'Diameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Diameter

        if temp is None:
            return None

        return temp

    @property
    def distance_along_fillet(self) -> 'float':
        """float: 'DistanceAlongFillet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DistanceAlongFillet

        if temp is None:
            return None

        return temp

    @property
    def face_width_position(self) -> 'float':
        """float: 'FaceWidthPosition' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidthPosition

        if temp is None:
            return None

        return temp

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Radius

        if temp is None:
            return None

        return temp

    @property
    def position(self) -> 'Vector3D':
        """Vector3D: 'Position' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Position

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value
