"""_1039.py

SurfaceRoughness
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility import _1390
from mastapy._internal.python_net import python_net_import

_SURFACE_ROUGHNESS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'SurfaceRoughness')


__docformat__ = 'restructuredtext en'
__all__ = ('SurfaceRoughness',)


class SurfaceRoughness(_1390.IndependentReportablePropertiesBase['SurfaceRoughness']):
    """SurfaceRoughness

    This is a mastapy class.
    """

    TYPE = _SURFACE_ROUGHNESS

    def __init__(self, instance_to_wrap: 'SurfaceRoughness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def fillet_roughness_rz(self) -> 'float':
        """float: 'FilletRoughnessRz' is the original name of this property."""

        temp = self.wrapped.FilletRoughnessRz

        if temp is None:
            return None

        return temp

    @fillet_roughness_rz.setter
    def fillet_roughness_rz(self, value: 'float'):
        self.wrapped.FilletRoughnessRz = float(value) if value else 0.0

    @property
    def flank_roughness_ra(self) -> 'float':
        """float: 'FlankRoughnessRa' is the original name of this property."""

        temp = self.wrapped.FlankRoughnessRa

        if temp is None:
            return None

        return temp

    @flank_roughness_ra.setter
    def flank_roughness_ra(self, value: 'float'):
        self.wrapped.FlankRoughnessRa = float(value) if value else 0.0

    @property
    def flank_roughness_rz(self) -> 'float':
        """float: 'FlankRoughnessRz' is the original name of this property."""

        temp = self.wrapped.FlankRoughnessRz

        if temp is None:
            return None

        return temp

    @flank_roughness_rz.setter
    def flank_roughness_rz(self, value: 'float'):
        self.wrapped.FlankRoughnessRz = float(value) if value else 0.0

    @property
    def flank_roughness_in_cla(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FlankRoughnessInCLA' is the original name of this property."""

        temp = self.wrapped.FlankRoughnessInCLA

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @flank_roughness_in_cla.setter
    def flank_roughness_in_cla(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FlankRoughnessInCLA = value

    @property
    def flank_roughness_in_rms(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'FlankRoughnessInRMS' is the original name of this property."""

        temp = self.wrapped.FlankRoughnessInRMS

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else None

    @flank_roughness_in_rms.setter
    def flank_roughness_in_rms(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.FlankRoughnessInRMS = value

    @property
    def is_flank_roughness_in_ra_estimated(self) -> 'bool':
        """bool: 'IsFlankRoughnessInRaEstimated' is the original name of this property."""

        temp = self.wrapped.IsFlankRoughnessInRaEstimated

        if temp is None:
            return None

        return temp

    @is_flank_roughness_in_ra_estimated.setter
    def is_flank_roughness_in_ra_estimated(self, value: 'bool'):
        self.wrapped.IsFlankRoughnessInRaEstimated = bool(value) if value else False

    @property
    def is_flank_roughness_in_rz_estimated(self) -> 'bool':
        """bool: 'IsFlankRoughnessInRzEstimated' is the original name of this property."""

        temp = self.wrapped.IsFlankRoughnessInRzEstimated

        if temp is None:
            return None

        return temp

    @is_flank_roughness_in_rz_estimated.setter
    def is_flank_roughness_in_rz_estimated(self, value: 'bool'):
        self.wrapped.IsFlankRoughnessInRzEstimated = bool(value) if value else False
