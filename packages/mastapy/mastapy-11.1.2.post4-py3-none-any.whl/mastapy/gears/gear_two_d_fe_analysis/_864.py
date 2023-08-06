"""_864.py

CylindricalGearTIFFAnalysis
"""


from mastapy.gears.gear_two_d_fe_analysis import _866
from mastapy._internal import constructor
from mastapy.gears.analysis import _1170
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TIFF_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearTIFFAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTIFFAnalysis',)


class CylindricalGearTIFFAnalysis(_1170.GearDesignAnalysis):
    """CylindricalGearTIFFAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_TIFF_ANALYSIS

    def __init__(self, instance_to_wrap: 'CylindricalGearTIFFAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis(self) -> '_866.CylindricalGearTwoDimensionalFEAnalysis':
        """CylindricalGearTwoDimensionalFEAnalysis: 'Analysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Analysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
