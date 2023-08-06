"""_865.py

CylindricalGearTIFFAnalysisDutyCycle
"""


from mastapy.gears.gear_two_d_fe_analysis import _866
from mastapy._internal import constructor
from mastapy.gears.analysis import _1170
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearTIFFAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTIFFAnalysisDutyCycle',)


class CylindricalGearTIFFAnalysisDutyCycle(_1170.GearDesignAnalysis):
    """CylindricalGearTIFFAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_TIFF_ANALYSIS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'CylindricalGearTIFFAnalysisDutyCycle.TYPE'):
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
