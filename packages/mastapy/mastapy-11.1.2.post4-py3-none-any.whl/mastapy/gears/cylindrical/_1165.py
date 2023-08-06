"""_1165.py

GearLTCAContactCharts
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_LTCA_CONTACT_CHARTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'GearLTCAContactCharts')


__docformat__ = 'restructuredtext en'
__all__ = ('GearLTCAContactCharts',)


class GearLTCAContactCharts(_0.APIBase):
    """GearLTCAContactCharts

    This is a mastapy class.
    """

    TYPE = _GEAR_LTCA_CONTACT_CHARTS

    def __init__(self, instance_to_wrap: 'GearLTCAContactCharts.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def depth_of_max_shear_stress(self) -> 'Image':
        """Image: 'DepthOfMaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DepthOfMaxShearStress

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def force_per_unit_length(self) -> 'Image':
        """Image: 'ForcePerUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForcePerUnitLength

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def gap_between_loaded_flanks_transverse(self) -> 'Image':
        """Image: 'GapBetweenLoadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GapBetweenLoadedFlanksTransverse

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def hertzian_contact_half_width(self) -> 'Image':
        """Image: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactHalfWidth

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def max_pressure(self) -> 'Image':
        """Image: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxPressure

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def max_shear_stress(self) -> 'Image':
        """Image: 'MaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaxShearStress

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def total_deflection_for_mesh(self) -> 'Image':
        """Image: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalDeflectionForMesh

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value
