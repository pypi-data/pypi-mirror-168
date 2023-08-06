"""_81.py

ShaftFEMeshingOptions
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _73, _58
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import

_SHAFT_FE_MESHING_OPTIONS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'ShaftFEMeshingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftFEMeshingOptions',)


class ShaftFEMeshingOptions(_58.FEMeshingOptions):
    """ShaftFEMeshingOptions

    This is a mastapy class.
    """

    TYPE = _SHAFT_FE_MESHING_OPTIONS

    def __init__(self, instance_to_wrap: 'ShaftFEMeshingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def corner_tolerance(self) -> 'float':
        """float: 'CornerTolerance' is the original name of this property."""

        temp = self.wrapped.CornerTolerance

        if temp is None:
            return None

        return temp

    @corner_tolerance.setter
    def corner_tolerance(self, value: 'float'):
        self.wrapped.CornerTolerance = float(value) if value else 0.0

    @property
    def meshing_diameter_for_gear(self) -> '_73.MeshingDiameterForGear':
        """MeshingDiameterForGear: 'MeshingDiameterForGear' is the original name of this property."""

        temp = self.wrapped.MeshingDiameterForGear

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_73.MeshingDiameterForGear)(value) if value is not None else None

    @meshing_diameter_for_gear.setter
    def meshing_diameter_for_gear(self, value: '_73.MeshingDiameterForGear'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MeshingDiameterForGear = value

    @property
    def minimum_fillet_radius_to_include(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MinimumFilletRadiusToInclude' is the original name of this property."""

        temp = self.wrapped.MinimumFilletRadiusToInclude

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @minimum_fillet_radius_to_include.setter
    def minimum_fillet_radius_to_include(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MinimumFilletRadiusToInclude = value

    @property
    def smooth_corners(self) -> 'bool':
        """bool: 'SmoothCorners' is the original name of this property."""

        temp = self.wrapped.SmoothCorners

        if temp is None:
            return None

        return temp

    @smooth_corners.setter
    def smooth_corners(self, value: 'bool'):
        self.wrapped.SmoothCorners = bool(value) if value else False
