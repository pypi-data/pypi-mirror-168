"""_1299.py

CirclesOnAxis
"""


from typing import List

from mastapy._math.vector_3d import Vector3D
from mastapy._internal import constructor, conversion
from mastapy._math.vector_2d import Vector2D
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_DOUBLE = python_net_import('System', 'Double')
_CIRCLES_ON_AXIS = python_net_import('SMT.MastaAPI.MathUtility', 'CirclesOnAxis')


__docformat__ = 'restructuredtext en'
__all__ = ('CirclesOnAxis',)


class CirclesOnAxis(_0.APIBase):
    """CirclesOnAxis

    This is a mastapy class.
    """

    TYPE = _CIRCLES_ON_AXIS

    def __init__(self, instance_to_wrap: 'CirclesOnAxis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axis(self) -> 'Vector3D':
        """Vector3D: 'Axis' is the original name of this property."""

        temp = self.wrapped.Axis

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @axis.setter
    def axis(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Axis = value

    @property
    def coord_fillet_radii(self) -> 'List[float]':
        """List[float]: 'CoordFilletRadii' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoordFilletRadii

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)
        return value

    @property
    def coords(self) -> 'List[Vector2D]':
        """List[Vector2D]: 'Coords' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Coords

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mouse_position(self) -> 'Vector2D':
        """Vector2D: 'MousePosition' is the original name of this property."""

        temp = self.wrapped.MousePosition

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)
        return value

    @mouse_position.setter
    def mouse_position(self, value: 'Vector2D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector2d(value)
        self.wrapped.MousePosition = value

    @property
    def origin(self) -> 'Vector3D':
        """Vector3D: 'Origin' is the original name of this property."""

        temp = self.wrapped.Origin

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @origin.setter
    def origin(self, value: 'Vector3D'):
        value = value if value else None
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Origin = value

    def add_coords(self, offset: 'float', radius: 'float'):
        """ 'AddCoords' is the original name of this method.

        Args:
            offset (float)
            radius (float)
        """

        offset = float(offset)
        radius = float(radius)
        self.wrapped.AddCoords.Overloads[_DOUBLE, _DOUBLE](offset if offset else 0.0, radius if radius else 0.0)

    def add_coords_from_point_on_axis(self, point_on_axis: 'Vector3D', radius: 'float'):
        """ 'AddCoords' is the original name of this method.

        Args:
            point_on_axis (Vector3D)
            radius (float)
        """

        point_on_axis = conversion.mp_to_pn_vector3d(point_on_axis)
        radius = float(radius)
        self.wrapped.AddCoords.Overloads[Vector3D, _DOUBLE](point_on_axis, radius if radius else 0.0)

    def add_coords_from_point_in_sketch_plane(self, point_in_sketch_plane: 'Vector3D'):
        """ 'AddCoords' is the original name of this method.

        Args:
            point_in_sketch_plane (Vector3D)
        """

        point_in_sketch_plane = conversion.mp_to_pn_vector3d(point_in_sketch_plane)
        self.wrapped.AddCoords.Overloads[Vector3D](point_in_sketch_plane)

    def add_fillet_point(self, point_a_in_sketch_plane: 'Vector3D', point_b_in_sketch_plane: 'Vector3D', guide_point: 'Vector3D', radius: 'float'):
        """ 'AddFilletPoint' is the original name of this method.

        Args:
            point_a_in_sketch_plane (Vector3D)
            point_b_in_sketch_plane (Vector3D)
            guide_point (Vector3D)
            radius (float)
        """

        point_a_in_sketch_plane = conversion.mp_to_pn_vector3d(point_a_in_sketch_plane)
        point_b_in_sketch_plane = conversion.mp_to_pn_vector3d(point_b_in_sketch_plane)
        guide_point = conversion.mp_to_pn_vector3d(guide_point)
        radius = float(radius)
        self.wrapped.AddFilletPoint(point_a_in_sketch_plane, point_b_in_sketch_plane, guide_point, radius if radius else 0.0)

    def set_mouse_position(self, point_in_sketch_plane: 'Vector3D'):
        """ 'SetMousePosition' is the original name of this method.

        Args:
            point_in_sketch_plane (Vector3D)
        """

        point_in_sketch_plane = conversion.mp_to_pn_vector3d(point_in_sketch_plane)
        self.wrapped.SetMousePosition(point_in_sketch_plane)
